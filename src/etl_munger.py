import csv
import json
import pathlib
from datetime import datetime
from typing import List, Set, Any

from pydantic import Field, field_validator, BaseModel, model_validator

from config_model import ConfigModel  # type: ignore
import yaml
import re
from decimal import Decimal

import logging

from operations import run_function  # type: ignore

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def try_cast_col(column: str, typ: str) -> Any:
    try:
        if typ == "integer":
            return int(column)
        elif typ == "string":
            return str(column)
        elif typ == "decimal":
            column = column.replace(",", "")
            return Decimal(column)
        elif typ == "date_yyyymmdd":
            return datetime(int(column[0:4]), int(column[4:6]), int(column[6:8])).date()
        elif typ == "datetime_yyyymmdd":
            return datetime(int(column[0:4]), int(column[4:6]), int(column[6:8]))
        elif typ == "two_digit_left_padded_string":
            return column.zfill(2)
        else:
            return column
    except Exception:
        return None


def write_data(data: List[List[str]], output_path: str) -> None:
    csv.writer(open(output_path, "w")).writerows(data)


class EtlMunger(BaseModel):
    config_path: str = Field(description="The path to the config file")
    config: ConfigModel = Field(default=None, exclude=True, description="The model for the config file")

    @field_validator("config_path")
    @classmethod
    def config_is_valid_path(cls, config_path: str) -> str:
        if not pathlib.Path(config_path).resolve(strict=True):
            raise ValueError("The config file path is not valid")
        if not (config_path.endswith(".yaml") or config_path.endswith(".yml") or config_path.endswith(".json")):
            raise ValueError("The config file must be a yaml, yml, or json file")
        return config_path

    @model_validator(mode="after")
    def load_config_file(self) -> 'EtlMunger':  # type: ignore
        if not pathlib.Path(self.config_path).resolve(strict=True):
            raise ValueError("The config file path is not valid")

        config = {}
        if self.config_path.endswith(".yaml") or self.config_path.endswith(".yml"):
            try:
                config = yaml.safe_load(open(self.config_path, 'r'))
            except Exception as e:
                raise ValueError(f"The yaml file is not valid: {e}") from e
        elif self.config_path.endswith(".json"):
            try:
                config = json.load(open(self.config_path, 'r'))
            except Exception as e:
                raise ValueError(f"The json file is not valid: {e}") from e
        self.config = ConfigModel(**config)
        return self

    def parse_and_write_files(self, input_path: str, output_path: str, failed_path: str | None = None) -> None:
        validated_data, failed_data = self.validate_and_transform(input_path)
        write_data(validated_data, output_path)
        if failed_path is not None:
            write_data(failed_data, failed_path)

    def _read_data(self, input_path: str) -> List[List[str]]:
        if self.config.file_config.type == "csv":
            return self._read_csv(input_path)
        else:
            raise ValueError("Only csv files are supported")

    def _read_csv(self, csv_path: str) -> List[List[str]]:
        with open(csv_path, mode='r') as file:
            if self.config.file_config.arguments is not None and self.config.file_config.arguments != {}:
                csv_reader = csv.reader(file, **self.config.file_config.arguments.dict())
            else:
                csv_reader = csv.reader(file)
            return [row for row in csv_reader]

    def _get_input_columns_needed(self) -> Set[str]:
        return {item for row in self.config.output_definition for item in row.input_columns
                if row.input_columns is not None}

    def _get_input_ids_needed(self, input_columns_needed: Set[str]) -> Set[int]:
        return {i for i, x in enumerate(self.config.input_definition) if x.name in input_columns_needed}

    def validate_and_transform(self, input_path: str) -> (List[List[Any]], List[List[Any]]):  # type: ignore

        raw_data = self._read_data(input_path)

        input_columns_needed = self._get_input_columns_needed()
        input_ids_needed = self._get_input_ids_needed(input_columns_needed)
        regex_list = [re.compile(x.regex) for i, x in enumerate(self.config.input_definition) if i in input_ids_needed]

        result: List[List[Any]] = [[x.alias for x in self.config.output_definition]]
        failed_rows: List[List[Any]] = []
        for r_id, row in enumerate(raw_data[1:]):
            validated_row = self._validate_and_cast_input(input_ids_needed, r_id, regex_list, row)

            if validated_row is None:
                failed_rows.append(row)
                continue

            transformed_row = self._transform_and_cast_for_output(r_id, validated_row)

            if transformed_row is None:
                failed_rows.append(row)
                continue
            result.append(transformed_row)

        return result, failed_rows

    def _transform_and_cast_for_output(self, r_id: int, validated_row: List[Any]) -> List[Any] | None:  # type: ignore
        input_name_to_id_map = {x.name: i for i, x in enumerate(self.config.input_definition)}
        transformed_row: List[Any] = []

        for output in self.config.output_definition:
            ids: List[int] = [input_name_to_id_map[x] for x in output.input_columns]
            if output.operation is not None:
                col = run_function(function=output.operation.function,
                                   column_values=[validated_row[i] for i in ids],
                                   args=output.operation.args,
                                   )
                if col is None:
                    logger.info(f"Row {r_id} failed operation validation")
                    return None
            else:
                col = validated_row[ids[0]]
            cast_column = try_cast_col(col, output.cast)
            if cast_column is None:
                logger.info(f"Row {r_id} failed type validation")
                return None
            else:
                transformed_row.append(cast_column)
        return transformed_row

    def _validate_and_cast_input(self,
                                 input_ids_needed: Set[int],
                                 r_id: int,
                                 regex_list: List[re.Pattern[str]],
                                 row: List[str]) -> List[Any] | None:  # type: ignore
        validated_row: List[str] = []

        for c_id, column in enumerate(row):
            if c_id not in input_ids_needed:
                continue

            if regex_list[c_id].match(column) is None:
                logger.info(f"Row {r_id} column {c_id} failed regex validation, failing early")
                return None
            cast_column = try_cast_col(column, self.config.input_definition[c_id].type)
            if cast_column is None:
                logger.info(f"Row {r_id} column {c_id} failed type validation, failing early")
                return None
            validated_row.append(cast_column)
        return validated_row
