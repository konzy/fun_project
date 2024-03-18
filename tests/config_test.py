from typing import Any, Dict

import pytest

from config_model import ConfigModel  # type: ignore
from copy import deepcopy

standard_config = {
    "file_config": {
        "type": "csv",
        "arguments": {
            "dialect": "excel",
            "delimiter": ",",
            "quotechar": "\"",
            "escapechar": None,
            "doublequote": True,
            "skipinitialspace": False,
            "lineterminator": "\r\n",
            "quoting": 0,
            "strict": False,
        },
    },
    "input_definition": [
        {
            "name": "name",
            "regex": "^[a-zA-Z]+$",
            "type": "string"
        },
        {
            "name": "age",
            "regex": "^[0-9]+$",
            "type": "integer"
        }
    ],
    "output_definition": [
        {
            "input_columns": ["name", "age"],
            "alias": "full_name",
            "cast": "string",
            "operation": {
                "function": "concat",
                "args": ["name", "age"]
            }
        }
    ]
}


file_config_success = deepcopy(standard_config)

@pytest.mark.parametrize("yaml_config", [
    file_config_success,
])
def test_load_yaml_success(yaml_config: Dict[str, Any]) -> None:
    cm = ConfigModel(**yaml_config)
    assert cm.file_config.type == "csv"
    assert cm.file_config.arguments.dialect == "excel"
    assert cm.file_config.arguments.delimiter == ","
    assert cm.file_config.arguments.quotechar == "\""
    assert cm.file_config.arguments.escapechar is None
    assert cm.file_config.arguments.doublequote is True
    assert cm.file_config.arguments.skipinitialspace is False
    assert cm.file_config.arguments.lineterminator == "\r\n"
    assert cm.file_config.arguments.quoting == 0
    assert cm.file_config.arguments.strict is False
    assert cm.input_definition[0].name == "name"
    assert cm.input_definition[0].regex == "^[a-zA-Z]+$"
    assert cm.input_definition[0].type == "string"
    assert cm.input_definition[1].name == "age"
    assert cm.input_definition[1].regex == "^[0-9]+$"
    assert cm.input_definition[1].type == "integer"
    assert cm.output_definition[0].input_columns == ["name", "age"]
    assert cm.output_definition[0].alias == "full_name"
    assert cm.output_definition[0].cast == "string"
    assert cm.output_definition[0].operation.function == "concat"
    assert cm.output_definition[0].operation.args == ["name", "age"]


file_config_missing = deepcopy(standard_config)
file_config_missing["file_config"] = None  # type: ignore

file_config_missing_type = deepcopy(standard_config)
file_config_missing_type["file_config"]["type"] = None  # type: ignore


@pytest.mark.parametrize("yaml_config", [
    file_config_missing,
    file_config_missing_type,
])
def test_load_yaml_fail_file_config(yaml_config: Dict[str, Any]) -> None:
    with pytest.raises(ValueError):
        ConfigModel(**yaml_config)


arguments_dialect_int = deepcopy(standard_config)
arguments_dialect_int["file_config"]["arguments"]["dialect"] = 1  # type: ignore

arguments_delimiter_int = deepcopy(standard_config)
arguments_delimiter_int["file_config"]["arguments"]["delimiter"] = 1  # type: ignore

arguments_quotechar_int = deepcopy(standard_config)
arguments_quotechar_int["file_config"]["arguments"]["quotechar"] = 1  # type: ignore

arguments_escapechar_int = deepcopy(standard_config)
arguments_escapechar_int["file_config"]["arguments"]["escapechar"] = 1  # type: ignore

arguments_doublequote_str = deepcopy(standard_config)
arguments_doublequote_str["file_config"]["arguments"]["doublequote"] = "string_value"  # type: ignore

arguments_skipinitialspace_str = deepcopy(standard_config)
arguments_skipinitialspace_str["file_config"]["arguments"]["skipinitialspace"] = "string_value"  # type: ignore

arguments_lineterminator_int = deepcopy(standard_config)
arguments_lineterminator_int["file_config"]["arguments"]["lineterminator"] = 1  # type: ignore

arguments_quoting_str = deepcopy(standard_config)
arguments_quoting_str["file_config"]["arguments"]["quoting"] = "string_value"  # type: ignore

arguments_strict_str = deepcopy(standard_config)
arguments_strict_str["file_config"]["arguments"]["strict"] = "string_value"  # type: ignore


@pytest.mark.parametrize("yaml_config", [
    arguments_dialect_int,
    arguments_delimiter_int,
    arguments_quotechar_int,
    arguments_escapechar_int,
    arguments_doublequote_str,
    arguments_skipinitialspace_str,
    arguments_lineterminator_int,
    arguments_quoting_str,
    arguments_strict_str,
])
def test_load_yaml_fail_arguments_wrong_type(yaml_config: Dict[str, Any]) -> None:
    with pytest.raises(ValueError):
        ConfigModel(**yaml_config)


input_definition_missing = deepcopy(standard_config)
input_definition_missing["input_definition"] = None  # type: ignore


@pytest.mark.parametrize("yaml_config", [
    input_definition_missing,
])
def test_load_yaml_fail_input_definition_missing(yaml_config: Dict[str, Any]) -> None:
    with pytest.raises(ValueError):
        ConfigModel(**yaml_config)


input_definition_name_wrong_type = deepcopy(standard_config)
input_definition_name_wrong_type["input_definition"][0]["name"] = 1  # type: ignore

input_definition_regex_wrong_type = deepcopy(standard_config)
input_definition_regex_wrong_type["input_definition"][0]["regex"] = 1  # type: ignore

input_definition_type_wrong_type = deepcopy(standard_config)
input_definition_type_wrong_type["input_definition"][0]["type"] = 1  # type: ignore


@pytest.mark.parametrize("yaml_config", [
    input_definition_name_wrong_type,
    input_definition_regex_wrong_type,
    input_definition_type_wrong_type,
])
def test_load_yaml_fail_input_definition_wrong_type(yaml_config: Dict[str, Any]) -> None:
    with pytest.raises(ValueError):
        ConfigModel(**yaml_config)


output_definition_missing = deepcopy(standard_config)
output_definition_missing["output_definition"] = None  # type: ignore


@pytest.mark.parametrize("yaml_config", [
    output_definition_missing,
])
def test_load_yaml_fail_output_definition_missing(yaml_config: Dict[str, Any]) -> None:
    with pytest.raises(ValueError):
        ConfigModel(**yaml_config)

output_definition_input_columns_wrong_type = deepcopy(standard_config)
output_definition_input_columns_wrong_type["output_definition"][0]["input_columns"] = 1  # type: ignore

output_definition_alias_wrong_type = deepcopy(standard_config)
output_definition_alias_wrong_type["output_definition"][0]["alias"] = 1  # type: ignore

output_definition_cast_wrong_type = deepcopy(standard_config)
output_definition_cast_wrong_type["output_definition"][0]["cast"] = 1  # type: ignore

output_definition_operation_function_wrong_type = deepcopy(standard_config)
output_definition_operation_function_wrong_type["output_definition"][0]["operation"]["function"] = 1  # type: ignore

output_definition_operation_args_wrong_type = deepcopy(standard_config)
output_definition_operation_args_wrong_type["output_definition"][0]["operation"]["args"] = 1  # type: ignore


@pytest.mark.parametrize("yaml_config", [
    output_definition_input_columns_wrong_type,
    output_definition_alias_wrong_type,
    output_definition_cast_wrong_type,
    output_definition_operation_function_wrong_type,
    output_definition_operation_args_wrong_type,
])
def test_load_yaml_fail_output_definition_wrong_type(yaml_config: Dict[str, Any]) -> None:
    with pytest.raises(ValueError):
        ConfigModel(**yaml_config)

