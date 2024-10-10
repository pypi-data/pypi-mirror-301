from __future__ import annotations

import io
import pathlib
from io import BytesIO
from typing import TYPE_CHECKING, Any, BinaryIO, Literal, Union

import numpy as np
import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.ipc as pa_ipc
import pyarrow.parquet as pq

from chalk.features._encoding.pyarrow import is_map_in_dtype_tree, pyarrow_to_polars
from chalk.utils.log_with_context import get_logger
from chalk.utils.missing_dependency import missing_dependency_exception

if TYPE_CHECKING:
    import polars as pl


_logger = get_logger(__name__)


class ArrowTableCastError(Exception):
    def __init__(self, errors: list[ArrowColumnCastError]):
        self.errors = errors
        super().__init__(f"Failed to cast columns: {errors}")


class ArrowColumnCastError(Exception):
    def __init__(self, msg: str, col_name: str, expected_dtype: pa.DataType, actual_dtype: pa.DataType):
        self.col_name = col_name
        self.expected_dtype = expected_dtype
        self.actual_dtype = actual_dtype
        super().__init__(
            f"Failed to cast column '{col_name}' from '{actual_dtype}' to '{expected_dtype}': {msg}",
        )


def is_binary_like(dtype: pa.DataType):
    return pa.types.is_binary(dtype) or pa.types.is_large_binary(dtype) or pa.types.is_fixed_size_binary(dtype)


def is_list_like(dtype: pa.DataType):
    return pa.types.is_list(dtype) or pa.types.is_large_list(dtype) or pa.types.is_fixed_size_list(dtype)


class PyArrowToPolarsConverter:
    """Convert a pyarrow table to a polars dataframe. Unlike ``pl.from_arrow``, this function correctly
    casts the schema where polars might otherwise choose the incorrect data type.

    This class requires the schema to be provided separately so the pyarrow-to-polars conversion expression
    can be cached
    """

    def __init__(self, schema: pa.Schema) -> None:
        super().__init__()
        self.schema = schema
        self.no_ext_schema = self._remove_extension_types(schema)
        self._pl_schema = {
            col_name: pyarrow_to_polars(schema.field(col_name).type, col_name) for col_name in schema.names
        }

    def _recursive_convert_map(self, arr: Union[pa.Array, pa.ChunkedArray]) -> pa.Array:
        """
        Recursively converts a `MapArray` to a `LargeList` of `StructArray`s,
        because `pl.from_arrow` cannot handle nested maps.
        (
            fails with:
               pyo3_runtime.PanicException: Arrow datatype Map(...) not supported by Polars.
               You probably need to activate that data-type feature.
        )
        """
        if isinstance(arr, pa.ChunkedArray):
            arr = arr.combine_chunks()

        if isinstance(arr, pa.MapArray):
            """
            ==================
            Original map array
            ==================

                MapArray
                    [
                        [
                           {key: abc, value: bbc},
                           {key: efg, value: hij},
                        ],
                        [
                           {key: ddd, value: bbc},
                           {key: zzz, value: hij},
                        ]
                    ]


                keys = [abc, efg, ddd, zzz]
                items = [bbc, hij, bbc, hij]
                offsets = [0, 2, 4]

            =========================
            Intermediate struct array
            =========================

                [
                    [
                       {key: abc, value: bbc},
                       {key: efg, value: hij},
                    ],
                    [
                       {key: ddd, value: bbc},
                       {key: zzz, value: hij},
                    ]
                ]

            ----------------------------------------
            To create from intermediate struct array:
            ----------------------------------------

                pa.ListArray.from_arrays([0, 2, 4], struct_array)

            """
            struct_arr = pa.StructArray.from_arrays(
                [arr.keys, self._recursive_convert_map(arr.items)], ["key", "value"]
            )
            list_arr = pa.LargeListArray.from_arrays(arr.offsets, struct_arr, mask=arr.is_null())
            return list_arr
        elif isinstance(arr, (pa.LargeListArray, pa.ListArray)):
            return pa.LargeListArray.from_arrays(
                arr.offsets, self._recursive_convert_map(arr.values), mask=arr.is_null()
            )
        elif isinstance(arr, pa.FixedSizeListArray):
            return pa.FixedSizeListArray.from_arrays(self._recursive_convert_map(arr.values), arr.type.list_size)
        elif isinstance(arr, pa.StructArray):
            return pa.StructArray.from_arrays(
                [self._recursive_convert_map(arr.field(i)) for i in range(arr.type.num_fields)],
                names=[arr.type[i].name for i in range(arr.type.num_fields)],
            )
        else:
            return arr

    def convert(self, table: pa.Table) -> pl.DataFrame:
        import polars as pl

        assert table.schema == self.schema, "The table schema differs from the declared schema"

        table = table.cast(self.no_ext_schema)

        # Polars cannot handle pa.float16, nor can pyarrow cast float16 to float32. So, we will manually cast float16 to float32 inside numpy
        # FIXME: While this should be recursive, in practice, we only encounter float16 inside of vector features
        new_cols: list[pa.Array | pa.ChunkedArray] = []
        for x in table.columns:
            if pa.types.is_float16(x.type):
                new_cols.append(pa.array(x.to_numpy(zero_copy_only=False).astype(np.dtype("float32"))))
                continue
            if pa.types.is_fixed_size_list(x.type):
                assert isinstance(x.type, pa.FixedSizeListType)
                if pa.types.is_float16(x.type.value_type):
                    as_array = x.combine_chunks()
                    assert isinstance(as_array, pa.FixedSizeListArray)
                    # We'll first expand all null elements into null lists of the correct length, and then convert to numpy
                    null_elements = as_array.is_null()
                    empty = pa.scalar(
                        np.empty((x.type.list_size,), dtype=np.dtype("float16")),
                        pa.list_(pa.float16(), x.type.list_size),
                    )
                    as_array = as_array.fill_null(empty)
                    pa_arr = pa.FixedSizeListArray.from_arrays(
                        as_array.flatten().to_numpy(zero_copy_only=False).astype(np.dtype("float32")),
                        x.type.list_size,
                    )
                    # Replace the filled empty elements with null
                    pa_arr = pc.if_else(  # type: ignore
                        null_elements, pa.scalar(None, pa.list_(pa.float32(), x.type.list_size)), pa_arr
                    )
                    new_cols.append(pa_arr)
                    continue
            if is_map_in_dtype_tree(x.type):
                new_cols.append(self._recursive_convert_map(x))
                continue
            new_cols.append(x)
        table = pa.Table.from_arrays(new_cols, table.column_names)

        try:
            df = pl.from_arrow(table, self._pl_schema)
        except Exception:
            _logger.debug(
                f"pl.from_arrow failed. Trying again after combining chunks and viewing, {table.num_rows=}, {table.nbytes=}, {table.schema=}",
                exc_info=True,
            )
            # Sometimes the table will have null buffers, which polars cannot handle. But it will work if we view it as itself
            # why? who knows
            table = pa.Table.from_pydict(
                {k: v.combine_chunks().view(v.type) for (k, v) in zip(table.column_names, table.columns)}
            )
            try:
                df = pl.from_arrow(table, self._pl_schema)
            except Exception:
                _logger.debug(
                    f"Trying to deal with table without chunking, {table.num_rows=}, {table.nbytes=}, {table.schema=}",
                    exc_info=True,
                )
                df = pl.from_arrow(table, rechunk=False, schema=self._pl_schema)

        assert isinstance(df, pl.DataFrame)
        col_name_to_expr = {
            col_name: pl.col(col_name).cast(expected_dtype).alias(col_name)
            for (col_name, actual_dtype) in df.schema.items()
            if (expected_dtype := self._pl_schema[col_name]) != actual_dtype
        }
        if len(col_name_to_expr) > 0:
            _logger.warning(f"PyArrow <-> polars schema mismatch for columns {', '.join(col_name_to_expr.keys())}")
            df = df.with_columns(list(col_name_to_expr.values()))
        return df

    @staticmethod
    def _source_type_of_extension_type(dtype: pa.DataType) -> pa.DataType:
        if isinstance(dtype, pa.ExtensionType):
            return dtype.storage_type
        return dtype

    @staticmethod
    def _remove_extension_types(table: pa.Schema) -> pa.Schema:
        return pa.schema(
            [
                pa.field(
                    name=field.name,
                    type=PyArrowToPolarsConverter._source_type_of_extension_type(field.type),
                    metadata=field.metadata,
                )
                for field in table
            ]
        )


def pa_table_to_pl_df(table: pa.Table[Any]) -> pl.DataFrame:
    return PyArrowToPolarsConverter(table.schema).convert(table)


def pa_array_to_pl_series(arr: pa.Array | pa.ChunkedArray) -> pl.Series:
    tbl = pa.Table.from_arrays([arr], ["col_0"])
    df = pa_table_to_pl_df(tbl)
    return df.get_column("col_0")


def pa_cast(table: pa.Table[Any], expected_schema: pa.Schema, collect_all_errors: bool = False) -> pa.Table[Any]:
    """Safely cast a pyarrow table to the expected schema. Unlike ``table.cast(schema)``, this function will reorder struct columns if needed"""
    table_column_names = list(table.column_names)
    table_col_name_to_col = {col_name: col for (col_name, col) in zip(table_column_names, table.columns)}
    expected_column_names = list(expected_schema.names)
    assert frozenset(expected_column_names).issubset(
        table_column_names
    ), f"The expected column names ({expected_column_names}) must be a subset of the table column names ({table_column_names})."
    if table.schema == expected_schema:
        # Short circuit
        return table
    # First let's select just the columns we're interested in
    table = table.select(expected_column_names)

    if table.schema == expected_schema:
        # Short circuit
        return table

    new_arrays: list[pa.ChunkedArray | pa.Array] = []

    errors: list[ArrowColumnCastError] = []
    for name, expected_type in zip(expected_column_names, expected_schema.types):
        col = table_col_name_to_col[name]
        assert isinstance(col, pa.ChunkedArray)
        if len(col) == 0:
            arr = pa.array([], expected_type)
            new_arrays.append(arr)
            continue

        casted_chunks = []
        for chunk in col.chunks:
            if len(chunk) == 0:
                continue
            try:
                chunk_res = _pa_cast_col(chunk, expected_type)
            except Exception as e:
                wrapped_error = ArrowColumnCastError(
                    msg=str(e), col_name=name, expected_dtype=expected_type, actual_dtype=chunk.type
                )
                if not collect_all_errors:
                    raise wrapped_error from e
                errors.append(wrapped_error)
            else:
                casted_chunks.append(chunk_res)
        if len(casted_chunks) == 0:
            arr = pa.nulls(0, expected_type)
        else:
            arr = pa.chunked_array(casted_chunks)
        new_arrays.append(arr)
    if errors:
        raise ArrowTableCastError(errors)

    return pa.Table.from_arrays(new_arrays, names=expected_schema.names)


def recursive_convert_map_primitive(x: Any, dtype: pa.DataType):
    """
    When we call polars `to_arrow` we end up with a DataFrame that
    has a bunch of maps or nested maps that are indistinguishable
    from list of structs of `key` and `value` fields. This function
    converts those list of dicts with `key` `value` fields into a dict,
    and they can then be faithfully converted into their `rich` form.
    """
    if x is None:
        return x
    if isinstance(dtype, pa.MapType):
        if not isinstance(x, list):
            raise ValueError(f"Expected a list, but got {type(x).__name__}")
        return {e["key"]: recursive_convert_map_primitive(e["value"], dtype.item_type) for e in x}
    elif isinstance(dtype, (pa.ListType, pa.LargeListType, pa.FixedSizeListType)):
        if not isinstance(x, list):
            raise ValueError(f"Expected a list, but got {type(x).__name__}")
        return [recursive_convert_map_primitive(y, dtype.value_type) for y in x]
    elif isinstance(dtype, pa.StructType):
        if not isinstance(x, dict):
            raise ValueError(f"Expected a dict, but got {type(x).__name__}")
        res = {}
        for k, v in x.items():
            field_idx = dtype.get_field_index(k)
            if field_idx == -1:
                raise ValueError(f"Missing field '{k}' in dtype '{dtype}'")
            res[k] = recursive_convert_map_primitive(v, dtype.field(field_idx).type)
        return res
    return x


def _recursive_convert_map_type(dtype: pa.DataType) -> pa.DataType:
    if pa.types.is_map(dtype):
        assert isinstance(dtype, pa.MapType)
        return pa.large_list(
            pa.struct(
                [
                    pa.field(name="key", type=dtype.key_type),
                    pa.field(name="value", type=_recursive_convert_map_type(dtype.item_type)),
                ]
            )
        )
    elif pa.types.is_large_list(dtype):
        assert isinstance(dtype, pa.LargeListType)
        return pa.large_list(_recursive_convert_map_type(dtype.value_type))
    elif pa.types.is_list(dtype):
        assert isinstance(dtype, pa.ListType)
        return pa.list_(_recursive_convert_map_type(dtype.value_type))
    elif pa.types.is_fixed_size_list(dtype):
        assert isinstance(dtype, pa.FixedSizeListType)
        return pa.list_(_recursive_convert_map_type(dtype.value_type), dtype.list_size)
    elif pa.types.is_struct(dtype):
        assert isinstance(dtype, pa.StructType)
        return pa.struct(
            [
                pa.field(
                    name=field.name,
                    type=_recursive_convert_map_type(field.type),
                    nullable=field.nullable,
                    metadata=field.metadata,
                )
                for field in dtype
            ]
        )
    return dtype


def _pa_cast_col(col: pa.Array, expected_type: pa.DataType) -> pa.Array:
    if col.null_count == len(col):
        # It's all null, so short circuit and return an array of nulls of the correct type
        # calling .flatten() sometimes will raise an exception if this condition is true
        return pa.nulls(len(col), expected_type)
    if is_map_in_dtype_tree(expected_type):
        expected_type = _recursive_convert_map_type(expected_type)
    if col.type == expected_type:
        return col
    if pa.types.is_struct(expected_type):
        # Convert the column to a table, then recursively cast the table
        assert isinstance(expected_type, pa.StructType)
        assert isinstance(col, pa.StructArray)
        arrays: list[pa.Array] = []
        names: list[str] = []
        fields: list[pa.Field] = []
        struct_type_as_schema = pa.schema(expected_type)
        for i in range(len(struct_type_as_schema)):
            field = struct_type_as_schema.field(i)
            fields.append(field)
            arrays.append(col.field(field.name))
            names.append(field.name)
        expected_sub_schema = pa.schema(fields)
        tbl = pa.Table.from_arrays(arrays, names)
        tbl = pa_cast(tbl, expected_sub_schema)
        # Now convert it back into a struct
        casted_columns = [x.combine_chunks() if isinstance(x, pa.ChunkedArray) else x for x in tbl.columns]
        struct_array = pa.StructArray.from_arrays(casted_columns, tbl.column_names)
        struct_array = struct_array.cast(expected_type)  # should be a no-op?
        return struct_array
    if pa.types.is_list(expected_type) or pa.types.is_large_list(expected_type):
        assert isinstance(expected_type, (pa.LargeListType, pa.ListType))
        assert isinstance(col, (pa.ListArray, pa.LargeListArray))
        flattened = col.flatten()
        tbl = pa.Table.from_arrays([flattened], names=[expected_type.value_field.name])
        tbl = pa_cast(tbl, pa.schema([expected_type.value_field]))
        casted_col = tbl.column(0).combine_chunks()
        assert len(flattened) == len(
            casted_col
        ), f"flattened has length {len(flattened)} but casted has length {len(casted_col)}"
        # col.offsets has random-looking values if the array has nulls. So we'll calculate the offsets
        # ourselves
        arr = col.value_lengths().fill_null(0)
        offsets: pa.Array = pc.cumulative_sum_checked(arr)  # type: ignore
        zero = pa.array([0], offsets.type)
        assert isinstance(zero, pa.Array)
        offsets = pa.concat_arrays([zero, offsets])
        mask = col.is_valid()
        single_true = pa.array([True], type=pa.bool_())
        assert isinstance(single_true, pa.Array)
        mask = pa.concat_arrays([mask, single_true])
        assert len(mask) == len(offsets)

        # Select the offset if the mask is True. Otherwise replace with null
        # This is per the docstring of ListArray.from_arrays
        # https://arrow.apache.org/docs/python/generated/pyarrow.ListArray.html#pyarrow.ListArray.from_arrays
        nulls = pa.nulls(len(offsets), offsets.type)
        offsets = pc.if_else(mask, offsets, nulls)  # type: ignore

        if pa.types.is_list(expected_type):
            if not isinstance(offsets, pa.Int32Array):
                offsets = offsets.cast(pa.int32())
            assert isinstance(offsets, pa.Int32Array)

            ans = pa.ListArray.from_arrays(offsets, casted_col)

        else:
            assert pa.types.is_large_list(expected_type)
            if not isinstance(offsets, pa.Int64Array):
                offsets = offsets.cast(pa.int64())
            assert isinstance(offsets, pa.Int64Array)
            ans = pa.LargeListArray.from_arrays(offsets, casted_col)

        assert len(ans) == len(col), "array should have the same number of elements"
        return ans
    if pa.types.is_fixed_size_list(expected_type):
        assert isinstance(expected_type, pa.FixedSizeListType)
        # We'll first expand all null elements into null lists of the correct length, and then convert to numpy
        null_elements = col.is_null()
        empty = pa.scalar(
            np.empty((expected_type.list_size,), dtype=expected_type.value_type.to_pandas_dtype()), expected_type
        )
        col = col.fill_null(empty)
        if isinstance(col, (pa.ListArray, pa.LargeListArray)):
            # Possible if we are coming from polars
            if pa.types.is_float16(expected_type.value_type):
                # For float16, we need to go to numpy
                flattened = pa.array(
                    col.flatten().to_numpy(zero_copy_only=False).reshape(-1).astype(np.dtype("float16"))
                )
            else:
                # For everything else, we go through python
                # Cannot go through numpy because ints will be cast to floats, since numpy doesn't have null
                # FIXME: Do this in c and skip python
                flattened = pa.array(col.to_pylist(), expected_type)
                assert isinstance(flattened, pa.FixedSizeListArray)
                flattened = flattened.flatten()
        else:
            assert isinstance(col.type, pa.FixedSizeListType)
            assert isinstance(col, pa.FixedSizeListArray)
            assert col.type.list_size == expected_type.list_size
            flattened = col.flatten()
        tbl = pa.Table.from_arrays([flattened], names=[expected_type.value_field.name])
        tbl = pa_cast(tbl, pa.schema([expected_type.value_field]))
        casted_col = tbl.column(0).combine_chunks()
        ans = pa.FixedSizeListArray.from_arrays(casted_col, expected_type.list_size)
        assert len(ans) == len(col), "array should have the same number of elements"
        # Replace the filled empty elements with null
        ans = pc.if_else(null_elements, pa.scalar(None, expected_type), ans)  # type: ignore
        return ans
    if pa.types.is_map(expected_type):
        return _pa_cast_col(col, expected_type)

    # Otherwise, cast directly if it's a scalar

    try:
        return col.cast(expected_type)
    except Exception as e:
        if pa.types.is_large_string(col.type) and pa.types.is_string(expected_type):
            _logger.error(
                f"Casting large string to large string instead of string like a maniac, {col.nbytes=}, {len(col)=}"
            )
            return col

        raise e


def _read_parquet(
    source: str | pathlib.Path | BinaryIO | BytesIO | bytes,
    **kwargs: Any,
):
    try:
        import polars as pl
    except ImportError:
        raise missing_dependency_exception("chalkpy[runtime]")

    if isinstance(source, str):
        if source.startswith("file://"):
            # Polars cannot handle local file uris properly
            source = source[len("file://") :]
        if source.startswith("gs://"):
            # Fsspec expects gcs instead of gs
            source = "gcs://" + source[len("gs://") :]
    return pl.read_parquet(source, **kwargs)


if TYPE_CHECKING:
    read_parquet = pl.read_parquet
else:
    read_parquet = _read_parquet


def record_batch_to_arrow_ipc(rb: pa.RecordBatch, compression: Literal["lz4", "zstd", "uncompressed"] = "lz4"):
    dest = BytesIO()
    writer = pa_ipc.RecordBatchFileWriter(dest, rb.schema, options=pa_ipc.IpcWriteOptions(compression=compression))
    writer.write_batch(rb)
    writer.close()
    dest.seek(0)
    feather_bytes = dest.read()
    return feather_bytes


def arrow_ipc_to_record_batch(b: bytes) -> pa.RecordBatch:
    bio = io.BytesIO(b)
    reader = pa_ipc.RecordBatchFileReader(bio)
    t: pa.Table = reader.read_all()
    return pa_table_to_recordbatch(t)


def pa_table_to_recordbatch(t: pa.Table) -> pa.RecordBatch:
    return pa.record_batch([c.combine_chunks() for c in t.columns], t.column_names)


def estimate_row_size_bytes(
    dtype: pa.DataType,
    *,
    average_string_size: int = 30,
    average_bytes_size: int = 100,
    average_list_length: int = 5,
    null_fraction: float = 0.0,
    float16_size: int = 2,
) -> float:
    """Estimate the average size of a row, given a schema. This is only slightly better than hardcoding logic based on row count, since it takes into account the width of the table.
    However, if the estimates for string, bytes, or list sizes are off, then this estimate could be way off. It assumes no nulls"""
    # Adding 0.125 to most fields to account for the nil bit
    if pa.types.is_null(dtype):
        return 0.125  # just the nil bit
    if pa.types.is_boolean(dtype):
        return 0.250  # bool bit + nil bit
    if pa.types.is_int8(dtype) or pa.types.is_uint8(dtype):
        return 1.125
    if pa.types.is_int16(dtype) or pa.types.is_uint16(dtype):
        return 2.125
    if (
        pa.types.is_int32(dtype)
        or pa.types.is_uint32(dtype)
        or pa.types.is_date32(dtype)
        or pa.types.is_time32(dtype)
        or pa.types.is_float32(dtype)
    ):
        return 4.125
    if (
        pa.types.is_int64(dtype)
        or pa.types.is_uint64(dtype)
        or pa.types.is_date64(dtype)
        or pa.types.is_time64(dtype)
        or pa.types.is_float64(dtype)
        or pa.types.is_timestamp(dtype)
        or pa.types.is_duration(dtype)
    ):
        return 8.125
    if pa.types.is_float16(dtype):
        return float16_size + 0.125
    if pa.types.is_string(dtype) or pa.types.is_large_string(dtype):
        return average_string_size + 0.125
    if pa.types.is_binary(dtype) or pa.types.is_large_binary(dtype):
        return average_bytes_size + 0.125
    if pa.types.is_fixed_size_binary(dtype):
        assert isinstance(dtype, pa.FixedSizeBinaryType)
        return dtype.byte_width + 0.125
    if pa.types.is_list(dtype) or pa.types.is_large_list(dtype) or pa.types.is_fixed_size_list(dtype):
        assert isinstance(dtype, (pa.ListType, pa.LargeListType, pa.FixedSizeListType))
        return (dtype.list_size if isinstance(dtype, pa.FixedSizeListType) else average_list_length) * (
            estimate_row_size_bytes(
                dtype.value_type,
                average_string_size=average_string_size,
                average_bytes_size=average_bytes_size,
                average_list_length=average_list_length,
                null_fraction=null_fraction,
                float16_size=float16_size,
            )
        ) + 0.125
    if pa.types.is_map(dtype):
        assert isinstance(dtype, pa.MapType)
        key_type = dtype.key_type
        value_type = dtype.item_type
        return (
            estimate_row_size_bytes(
                key_type,
                average_string_size=average_string_size,
                average_bytes_size=average_bytes_size,
                average_list_length=average_list_length,
                null_fraction=null_fraction,
                float16_size=float16_size,
            )
            + estimate_row_size_bytes(
                value_type,
                average_string_size=average_string_size,
                average_bytes_size=average_bytes_size,
                average_list_length=average_list_length,
                null_fraction=null_fraction,
                float16_size=float16_size,
            )
        ) * average_list_length + 0.125
    if pa.types.is_struct(dtype):
        assert isinstance(dtype, pa.StructType)
        size = 0.125
        for i in range(dtype.num_fields):
            f = dtype.field(i)
            size += estimate_row_size_bytes(
                f.type,
                average_string_size=average_string_size,
                average_bytes_size=average_bytes_size,
                average_list_length=average_list_length,
                null_fraction=null_fraction,
                float16_size=float16_size,
            )
        return size

    # If there's a type we didn't handle, assume 4 bytes
    return 4.125


def write_table_to_parquet(table: pa.Table, compression: str = "snappy") -> io.BytesIO:
    buffer = io.BytesIO()
    # From https://cloud.google.com/bigquery/docs/loading-data-cloud-storage-parquet#input_file_requirements,
    # row sizes need to be less than 50MB. I presume they meant to say row GROUP sizes in the docs, not individual row
    # sizes. Assuming each row is approximately the same size, we can determine an appropriate row group size
    if len(table) == 0:
        # Doesn't really matter since there is no data!
        target_row_group_size = 1
    else:
        avg_bytes_per_row = table.nbytes / len(table)
        max_bytes_per_row_group = 50 * 1024 * 1024
        avg_row_group_size = max_bytes_per_row_group / avg_bytes_per_row
        # FIXME: Pick the target row group size via statistics. But I think targeting for 25MB row groups (i.e. half of the allowance)
        # should be pretty safe
        target_row_group_size = int(avg_row_group_size // 2)
        # The default row group size is 1024*1024 (https://arrow.apache.org/docs/python/generated/pyarrow.parquet.write_table.html#pyarrow.parquet.write_table)
        # Let's never exceed that
        target_row_group_size = min(1024 * 1024, target_row_group_size)
        # But let's always have at least one row
        target_row_group_size = max(target_row_group_size, 1)
    pq.write_table(
        table,
        buffer,
        compression=compression,
        use_compliant_nested_type=True,
        row_group_size=target_row_group_size,
    )
    buffer.seek(0)
    return buffer


def describe_type_of_dataframe(frame: pl.DataFrame | pa.Table) -> str:
    description = f"DataFrame shape=({frame.shape[0]} rows, {frame.shape[1]} cols)"

    if isinstance(frame, pa.Table):
        frame_columns = frame.column_names  # pyright: ignore[reportAttributeAccessIssue]
    else:
        frame_columns = frame.columns

    if len(frame_columns) > 0:
        if len(frame_columns) < 20:
            description += f" with columns {repr(frame_columns)}"
        else:
            description += f" with selected columns {repr(frame_columns[:20])}"

    return description


def to_pydict(arrow_obj: pa.RecordBatch | pa.Table, /):
    """Convert an arrow object to a python list using our optimized impl"""
    return dict(zip(arrow_obj.column_names, (to_pylist(x) for x in arrow_obj.columns)))


def to_pylist(arrow_obj: pa.Array | pa.ChunkedArray, /) -> list[object]:
    """Convert an arrow object to a python list using our optimized impl"""
    try:
        from libchalk.utils import (  # pyright: ignore[reportMissingModuleSource,reportMissingImports]
            arrow_array_to_pylist,
        )
    except ImportError:
        return arrow_obj.to_pylist()
    else:
        if isinstance(arrow_obj, pa.ChunkedArray):
            ans: list[object] = []
            for chunk in arrow_obj.chunks:
                if isinstance(chunk, pa.ExtensionArray):
                    assert isinstance(
                        arrow_obj.type, pa.ExtensionType
                    ), "ExtensionArray must have an ExtensionType type."
                    chunk = chunk.storage.cast(arrow_obj.type.storage_type)
                ans.extend(arrow_array_to_pylist(chunk))
            return ans
        elif isinstance(arrow_obj, pa.ExtensionArray):
            assert isinstance(arrow_obj.type, pa.ExtensionType), "ExtensionArray must have an ExtensionType type."
            arrow_obj = arrow_obj.storage.cast(arrow_obj.type.storage_type)
        return arrow_array_to_pylist(arrow_obj)
