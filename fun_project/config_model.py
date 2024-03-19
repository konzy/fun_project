from enum import Enum
from typing import List
from pydantic import BaseModel, Field


class CastType(str, Enum):
    string = "string"
    integer = "integer"
    column = "column"
    decimal = "decimal"
    datetime_yyyymmdd = "datetime_yyyymmdd"
    date_yyyymmdd = "date_yyyymmdd"
    two_digit_left_padded_string = "two_digit_left_padded_string"


class InputDef(BaseModel):
    name: str = Field(description="The name of the input column")
    regex: str = Field(description="The validation for the column, this is a regex")
    type: str = Field(default=None, description="The type of the column, for example int, string, date, etc")


class Operation(BaseModel):
    function: str = Field(description="The function to do the transformation")
    args: List[str] | None = Field(default=None, description="The arguments for the function, if any")


class OutputDef(BaseModel):
    input_columns: List[str] | List = Field(default=list(), description="The input columns for this output column")
    alias: str = Field(description="The name of the output column")
    cast: CastType = Field(default=CastType.string, description="The type to cast the output column to")
    operation: Operation | None = Field(default=None, description="The operation to do on the input columns to get the "
                                                                  "output column")


class CsvArgs(BaseModel):
    dialect: str = "excel"
    delimiter: str = ","
    quotechar: str | None = '\"'
    escapechar: str | None = None
    doublequote: bool = True
    skipinitialspace: bool = False
    lineterminator: str = "\r\n"
    quoting: int = 0
    strict: bool = False


class FileConfig(BaseModel):
    type: str = Field(default="csv", description="The type of the file, for example csv, parquet, etc")
    arguments: CsvArgs | None = Field(default=None, description="The arguments for the file type")


class ConfigModel(BaseModel):
    file_config: FileConfig
    input_definition: List[InputDef]
    output_definition: List[OutputDef]
