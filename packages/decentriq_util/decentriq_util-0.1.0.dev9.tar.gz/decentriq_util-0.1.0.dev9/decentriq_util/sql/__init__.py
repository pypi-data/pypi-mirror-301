import typing
from typing import Tuple, List
import os
import numpy
import pandas as pd

from .proto.compute_sql_pb2 import (
    TableSchema,
    PrimitiveType,
    NamedColumn,
    ColumnType
)
from ..proto import (
    parse_length_delimited,
    serialize_length_delimited
)

__pdoc__ = {
    "proto": False,
}


datatype_mapping = {
    PrimitiveType.INT64: pd.Int64Dtype(),
    PrimitiveType.STRING: str,
    PrimitiveType.FLOAT64: numpy.float64,
}


datatype_mapping_reverse = {
    "Int64": PrimitiveType.INT64,
    "int64": PrimitiveType.INT64,
    "object": PrimitiveType.STRING,
    "float64": PrimitiveType.FLOAT64
}


DATASET_FILE_NAME = "dataset.csv"
SCHEMA_FILE_NAME = "types"


def _get_numpy_dtypes_for_table_schema_object(
        schema,
        use_numpy_int_type: bool = False
) -> List[Tuple[str, numpy.dtype]]:
    ix = 1
    columns = []
    for col in schema.namedColumns:
        # This matches R convention, unnamed columns get a position
        name = col.name if col.name else f"V{ix}"
        sql_type = col.columnType.primitiveType
        if sql_type == PrimitiveType.INT64 and use_numpy_int_type:
            dtype = numpy.int64
        else:
            dtype = datatype_mapping[sql_type]
        columns.append((name, dtype))
        ix += 1

    return columns


def _get_numpy_dtypes_for_table_schema(
        schema_path: str,
        use_numpy_int_type: bool = False
) -> List[Tuple[str, numpy.dtype]]:
    with open(schema_path, "rb") as f:
        schema = TableSchema()
        parse_length_delimited(f.read(), schema)

    return _get_numpy_dtypes_for_table_schema_object(schema, use_numpy_int_type)


def _get_table_schema_for_data_frame(df: pd.DataFrame) -> TableSchema:
    dtypes_as_string = [str(dtype) for dtype in df.dtypes]
    proto_columns = []
    for name, dtype in zip(list(df.columns), dtypes_as_string):
        primitive_type = datatype_mapping_reverse[dtype]
        column = NamedColumn(
            name=name,
            columnType=ColumnType(
                primitiveType=primitive_type,
                nullable=True
            )
        )
        proto_columns.append(column)
    return TableSchema(
        namedColumns=proto_columns
    )


def _assert_files_do_exist(dataset_file: str, schema_file: str) -> None:
    if not os.path.exists(dataset_file):
        raise Exception(
            f"Cannot read data from {dataset_file}, file containing data"
            f" {dataset_file} does not exist!"
        )
    if not os.path.exists(schema_file):
        raise Exception(
            f"Cannot read data from {dataset_file}, file encoding schema"
            f" {schema_file} does not exist!"
        )


def _assert_files_dont_exist(dataset_file: str, schema_file: str):
    if os.path.exists(dataset_file):
        raise Exception(
            "Cannot write data to {path}, file containing data"
            f" {dataset_file} already exists!"
        )
    if os.path.exists(schema_file):
        raise Exception(
            "Cannot write data to {path}, file encoding schema"
            f" {schema_file} already exists!"
        )


def read_tabular_data(path: str) -> pd.DataFrame:
    """
    Read data from a tabular input node or as written by an SQL computation.

    The input file must not contain a header row!

    Empty values for columns of type TEXT are replaced with empty strings.

    Empty values in columns of type INT64 are read as the "pandas.NA" value.
    For more information, please refer to the
    [pandas documentation](https://pandas.pydata.org/pandas-docs/dev/user_guide/integer_na.html).
    """
    return read_sql_data_from_dir(path)


def read_sql_data_from_dir(path: str) -> pd.DataFrame:
    """
    Note: this function is deprecated, use the function `read_tabular_data`.

    This function uses the previous `read_sql_data` function to convert
    the standard format of validated tabular input datasets and the output
    of SQL computations into a pandas dataframe, automatically importing the
     headers the are contained in the `types` file as well. One example below:
    ```python
    import decentriq_util.sql as dqu
    import pandas as pd

    dataframe_1 = dqu.read_sql_data_from_dir("/input/mySQLComputation")
    dataframe_2 = dqu.read_sql_data_from_dir("/input/myTabularDataset")
    ```
    """
    dataset_file = os.path.join(path, DATASET_FILE_NAME)
    schema_file = os.path.join(path, SCHEMA_FILE_NAME)
    _assert_files_do_exist(dataset_file, schema_file)
    return read_sql_data(dataset_file, schema_file)


def write_tabular_data(df: pd.DataFrame, path: str = "/output"):
    """
    Write a Pandas dataframe into the given directory in a format compatible
    with downstream SQL computation. This function allows you to use the output of
    a python computation as input to a SQL computation.
    For example:

    ```python
    import decentriq_util.sql as dqu
    import pandas as pd

    my_dataframe = pd.DataFrame()
    ...
    dqu.write_tabular_data(my_dataframe)
    ```
    """
    write_sql_data_to_dir(df, path)


def write_sql_data_to_dir(df: pd.DataFrame, path: str):
    """
    Note: this function is deprecated, use the function `write_tabular_data`.

    Write a Pandas dataframe into the given directory in a format compatible
    with downstream SQL computations. This function allows you to use the output of
    a python computation as input to a SQL computation.
    To do so, you will need to use `/output` as path.

    For example:
    ```python
    import decentriq_util.sql as dqu
    import pandas as pd

    my_dataframe = pd.DataFrame()
    ...
    dqu.write_sql_data_to_dir(my_dataframe, "/output")
    ```
    """
    dataset_file = os.path.join(path, DATASET_FILE_NAME)
    schema_file = os.path.join(path, SCHEMA_FILE_NAME)
    _assert_files_dont_exist(dataset_file, schema_file)
    return write_sql_data(df, dataset_file, schema_file)


def read_sql_data(data_path: str, schema_path: str) -> pd.DataFrame:
    """
    Read data as output by the SQL validation node.

    The input file must not contain a header row!

    Empty values for columns of type TEXT are replaced with empty strings.

    Empty values in columns of type INT64 are read as the "pandas.NA" value.
    For more information, please refer to the
    [pandas documentation](https://pandas.pydata.org/pandas-docs/dev/user_guide/integer_na.html).
    """
    _assert_files_do_exist(data_path, schema_path)
    columns = _get_numpy_dtypes_for_table_schema(schema_path)
    dtype_per_column = {
        ix: column_type
        for ix, (_, column_type) in enumerate(columns)
    }
    try:
        # First read just the data.
        # Tell the type linter that the value is in fact a DataFrame
        # as it could be a TextParser object depending on whether either
        # `chunksize` or `iterator` arguments are specified.
        original_data = typing.cast(
            pd.DataFrame,
            pd.read_csv(
                data_path,
                index_col=None,
                header=None, # sql verifier doesn't write headers
                dtype=str    # treat everything as string at first
            )
        )
        # Read the schema file that tells us about the data types.
        # Replace NaN values with empty strings for string-type columns.
        string_column_replacements =\
            {ix: "" for ix, dtype in dtype_per_column.items() if dtype == str}
        original_data.fillna(string_column_replacements, inplace=True)
        # Check whether the DF is empty now (even if it wasn't in the beginning)
        # If yes, return an empty DF.
        if original_data.shape[0] == 0:
            return pd.DataFrame(
                { name: pd.Series(dtype=dtype) for name, dtype in columns }
            )
        else:
            # Convert columns to the correct dtype
            for ix, dtype in dtype_per_column.items():
                if original_data[ix].dtype != dtype:
                    original_data[ix] = original_data[ix].astype(dtype)
    except pd.errors.EmptyDataError:
        return pd.DataFrame(
            { name: pd.Series(dtype=dtype) for name, dtype in columns }
        )
    header = [column_name for column_name, _ in columns]
    original_data.columns = header

    return original_data


def write_sql_data(df: pd.DataFrame, data_path: str, schema_path: str):
    """
    Write a Pandas dataframe to the given path, and store its schema including column names at
    `schema_path` with the protobuf standard used in the cross-workers interactions.
    """
    _assert_files_dont_exist(data_path, schema_path)
    schema = _get_table_schema_for_data_frame(df)
    schema_serialized = serialize_length_delimited(schema)
    df.to_csv(data_path, index=False, header=False, sep=",")
    with open(schema_path, "wb") as f:
        f.write(schema_serialized)
