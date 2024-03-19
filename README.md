# Overview

This is a simple project that allows the user to use a yaml or json file to configure a simple ETL pipeline.
The pipeline is composed of three main components::

## Yaml File Structure
file_config: This is the configuration for the input file. It allows for the user to specify the file path, the delimiter, and the quote character.
```yaml
file_config:
  type: "csv"
  arguments:
    dialect: "excel"
    delimiter: ","
    quotechar: '\"'
    escapechar: None
    doublequote: True
    skipinitialspace: False
    lineterminator: "\r\n"
    quoting: 0
    strict: False
```

input_definition: This defines the input data for each input column. The name key is not important for csv files, but could be used in the future for other file types.

The regex key is used to make sure that the input data conforms to a regular expression. Make sure to use ^ and \\Z$ to make sure that python makes sure that it checks from the beginning to the end of the string without including a newline character.

The type key is used to regularize the input data. For example, if the input data is a two digit number, it would be regularized to a two digit left padded string. This allows for flexibility in the input data without needing to make the output transformations more complex.
```yaml
input_definition:
  - name: Month
    regex: "^\\d{1,2}\\Z$"
    type: two_digit_left_padded_string
```

output_definition: This defines the output data for each output column.

The input_columns key is used to define the input columns that will be used in the operation.

The alias key is used to define the name of the output column.

The cast key is used to define the type of the output column. This can be used when using the package to get the data as an object, or when outputting filetypes that retain column type data.

The operation key is used to define the operation that will be used to transform the input columns into the output column. The function key is used to define the function that will be used to transform the input columns into the output column. The args key is used to define the arguments that will be used in the function.
```yaml
output_definition:
  - input_columns: ["Year", "Month", "Day"]
    alias: OrderDate
    cast: date_yyyymmdd
    operation:
      function: concat
      args:
        - Year
        - Month
        - Day
```

## Pipeline
Here are the steps of the pipeline:

1. Input: Reads the csv file row by row
2. RegEx and Regularize: Validate each column and conform to a standard format, this is done to the entire row before moving on, if there are any errors, it fails on the first one.
3. Operate, Cast and Alias: Perform operations on the columns, cast it to a type and name the column.

I wrote the pipeline in this way to be the most performant and to fail fast.
If there are any errors, it will fail on the first one for each row.
Also, it only does a single pass of the file.
This is about as fast as it can go without using a database or a package like Polars or Spark.

### Assumptions
1. Input data is a csv file with a header row.
2. All input columns are defined in the configuration file.
3. The configuration file should have the raw regex
4. The csv file is properly formed and has the same number of columns as the configuration file.
5. Log errors
6. Write two different files, one with the errors and one with the output data.
7. The output file will be a csv file with a header row.
8. Fail fast, if there are any errors, it will fail on the first one for each row.
9. As a package also allow for the user to get the data as an object.

### Future Work
If this was a real project, I'd use a package like Polars, Spark, or the database itself like Snowflake depending on the size of data and where it's located.

I'd also use DBT to write the transformations, and Airflow to schedule the pipeline.

I'd also use a package like Great Expectations to validate the data on the input and output.

I'd also abstract the input regex to make them standard across the project so that they can be reused.

# Dev Stuff

## Packages
I used the following packages:
- PyYAML for parsing the yaml file
- csv for reading and writing the csv file
- mypy for type checking
- ruff for linting, pep8 and type checking
- pytest for testing
- pre-commit for running tests and linting before committing
- poetry for package management
- Pydantic for modeling the data

## Running the Project
Install dependencies using poetry and switch to the virtual environment
```bash
poetry install
poetry shell
```

Run the example
```bash
cd fun_project/examples
python example_get_objects.py
python example_write_file.py
```
The first example will get the data as an object and print it out to stdout. The second example will write the data to two files, out/failed.csv and out/output.csv.

To run tests for MyPy, Pytest, Ruff and others
```bash
pre-commit
```

To get coverage
```bash
coverage report -m
```

If you'd like to contribute, install pre-commit hooks
```bash
pre-commit install
```
