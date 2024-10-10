from pyspark.sql import Row
from pyspark.sql.functions import *
from pyspark.sql.types import StructField
from easy_spark.easy_delta_helpers import EasyDeltaHelpers
from easy_spark.easy_sql_builder import EasySQLSelectBuilder
from easy_spark.lh_path import LHPath
from easy_spark.table_path import TablePath
from pyspark.sql import SparkSession
from easy_spark.wh_path import WHPath
from datetime import datetime
import numpy as np
from pandas import DataFrame as DataFramePandas
import pandas as pd


class EasyDF:
    _spark: SparkSession = None

    # Constructor
    def __init__(self, df: DataFrame = None, spark: SparkSession = None):
        self._df: DataFrame = df
        if spark is not None:
            EasyDF._spark = spark

    @staticmethod
    def create(spark: SparkSession, df: DataFrame = None) -> 'EasyDF':
        return EasyDF(df, spark)

    @staticmethod
    def create_empty(spark: SparkSession, schema: StructType = None) -> 'EasyDF':
        return EasyDF(None, spark).empty(schema)

    @property
    def df(self) -> DataFrame:
        return self._df

    @df.setter
    def df(self, value: DataFrame):
        self._df = value

    @property
    def current_schema(self) -> StructType:
        return self._df.schema if self._df and self._df.schema else None

    def from_table_path(self, path: TablePath, df_format="delta") -> 'EasyDF':
        self._df = EasyDF._spark.read.format(df_format).load(path.path)
        return self

    def from_path(self, path: str, df_format="delta") -> 'EasyDF':
        self._df = EasyDF._spark.read.format(df_format).load(path)
        return self

    def from_lh_table(self, name: str, table_name: str, limit: int = None) -> 'EasyDF':
        sql_builder = EasySQLSelectBuilder.new().select(["*"]).from_lh_table(name, table_name).limit(limit)
        return self.from_sql(sql_builder.sql)

    def from_lh_name_path(self, name: str, table_name: str, limt: int = None) -> 'EasyDF':
        if limt:
            self._df = EasyDF._spark.sql(f"SELECT * FROM {name}.{table_name} LIMIT {limt}")
        else:
            self._df = EasyDF._spark.sql(f"SELECT * FROM {name}.{table_name}")

        return self

    def from_sql_builder(self, sql_builder: EasySQLSelectBuilder) -> 'EasyDF':
        return self.from_sql(sql_builder.sql)

    def from_lh_flat_path(self, path: tuple[str, str, str, str], df_format="delta") -> 'EasyDF':
        from easy_spark.path import Path
        return self.from_table_path(LHPath(Path(path[0], path[1]), path[2], path[3]), df_format)

    def from_wh_flat_path(self, path: tuple[str, str, str, str], df_format="delta") -> 'EasyDF':
        from easy_spark.path import Path
        return self.from_table_path(WHPath(Path(path[0], path[1]), path[2], path[3]), df_format)

    def from_dict(self, records: dict, schema: StructType = None) -> 'EasyDF':
        new_schema = schema if schema is not None else self.current_schema
        self._df = EasyDF._spark.createDataFrame([Row(**records)], new_schema)
        return self

    def from_list(self, records: list[dict], schema: StructType = None, ignore_order=False) -> 'EasyDF':
        new_schema = schema if schema is not None else self.current_schema

        if ignore_order:
            rows = [Row(**record) for record in records]
            self._df = EasyDF._spark.createDataFrame(rows, new_schema)
        else:
            pdf_df = pd.DataFrame(records)
            self.from_pandas(pdf_df, new_schema)

        return self

    def from_tuple(self, records: list[tuple], schema: StructType = None) -> 'EasyDF':
        new_schema = schema if schema is not None else self.current_schema
        self._df = EasyDF._spark.createDataFrame(records, new_schema)
        return self

    def from_sql(self, sql: str) -> 'EasyDF':
        self._df = EasyDF._spark.sql(sql)
        return self

    def from_json(self, json: str) -> 'EasyDF':
        self._df = EasyDF._spark.read.json(json)
        return self

    def from_csv(self, csv_path: str, header=True, seperator=",", infer_schema=True) -> 'EasyDF':
        self._df = EasyDF._spark.read.option("header", header).csv(csv_path, sep=seperator, inferSchema=infer_schema)

        return self

    def from_pandas(self, pd_df: DataFramePandas, schema: StructType = None) -> 'EasyDF':
        new_schema = schema if schema is not None else self.current_schema
        self._df = EasyDF._spark.createDataFrame(pd_df, new_schema)

        return self

    def from_instance_sql_builder(self):
        pass

    def clear(self) -> 'EasyDF':
        self._df = EasyDF._spark.createDataFrame([], StructType([]))

        return self

    def empty(self, schema: StructType = None) -> 'EasyDF':
        new_schema = schema if schema is not None else self.current_schema
        self._df = EasyDF._spark.createDataFrame([], new_schema)

        return self

    def filter_by_filter(self, condition: str) -> 'EasyDF':
        if condition:
            self._df = self._df.filter(condition)
        return self

    def filter_by_any(self, condition: any) -> 'EasyDF':
        if condition:
            self._df = self._df.filter(condition)
        return self

    def filter(self, keys: dict[str, any] = None):
        if keys:
            for key in keys:
                self._df = self._df[self._df[key] == keys[key]]

        return self

    def filter_using_filter(self, keys: dict[str, any] = None):
        if keys:
            conditions = EasyDeltaHelpers.build_condition(keys)
            self._df = self._df.filter(conditions)

        return self

    def where_using_where(self, keys: dict[str, any] = None) -> 'EasyDF':
        if keys:
            conditions = EasyDeltaHelpers.build_condition(keys)
            self._df = self._df.where(conditions)
        return self

    def where(self, condition: str) -> 'EasyDF':
        if condition:
            self._df = self._df.where(condition)
        return self

    def where_by_any(self, condition: any) -> 'EasyDF':
        if condition:
            self._df = self._df.where(condition)
        return self

    def combine_from_df(self, df: DataFrame, type: str = 'unionByName',
                        allowMissingColumns: bool = True) -> 'EasyDF':
        self._df = EasyDeltaHelpers.combine_from_dfs([self._df, df], type, allowMissingColumns)
        return self

    def combine_from_pd_df(self, pd_df: DataFramePandas, schema: StructType = None, type: str = 'unionByName',
                           allowMissingColumns: bool = True) -> 'EasyDF':
        new_schema = schema if schema is not None else self.current_schema
        df = EasyDF._spark.createDataFrame(pd_df, new_schema)
        return self.combine_from_df(df, type, allowMissingColumns)

    def replace_column_empty_spaces(self, value="") -> 'EasyDF':
        for col_name in self._df.columns:
            self._df = self._df.withColumnRenamed(col_name, col_name.replace(" ", value))
        return self

    def replace_column_invalid_chars(self, invalid_chars=",;{}()", value="") -> 'EasyDF':
        for col_name in self._df.columns:
            current_col_name = col_name
            for c in invalid_chars:
                current_col_name = current_col_name.replace(c, value)
            self._df = self._df.withColumnRenamed(col_name, current_col_name)

        return self

    def replace_column(self, from_value="", value="") -> 'EasyDF':
        for col_name in self._df.columns:
            current_col_name = col_name
            current_col_name = current_col_name.replace(from_value, value)
            self._df = self._df.withColumnRenamed(col_name, current_col_name)

        return self

    def rename_columns(self, values: dict[str, str]):
        for col_name in self._df.columns:
            if col_name in values:
                self._df = self._df.withColumnRenamed(col_name, values[col_name])

        return self

    def drop_column_if_exists(self, column_name: str) -> 'EasyDF':
        if column_name in self._df.columns:
            self._df = self._df.drop(column_name)
        return self

    def add_column(self, column_name: str, value: any) -> 'EasyDF':
        self._df = self._df.withColumn(column_name, lit(value))
        return self

    def capitalize_column_between_spaces(self) -> 'EasyDF':
        for col_name in self._df.columns:
            current_col_name = col_name
            # Capitalize the first letter of each word
            for word in current_col_name.split(" "):
                current_col_name = current_col_name.replace(word, word.capitalize())
            self._df = self._df.withColumnRenamed(col_name, current_col_name)

        return self

    def title_columns(self) -> 'EasyDF':
        for col_name in self._df.columns:
            self._df = self._df.withColumnRenamed(col_name, col_name.title())

        return self

    def replace_nan(self, value=None) -> 'EasyDF':
        self._df = self._df.replace({np.nan: value}).replace({"nan": value})

        return self

    def overwrite_types(self, struct_types: dict | list[StructField] = None) -> 'EasyDF':
        struct_types = EasyDeltaHelpers.build_struct_fields(struct_types)

        for struct_t in struct_types:
            filed_r = struct_t.name.replace("`", "")
            # Check if field is in df
            if filed_r not in self._df.columns:
                continue
            self._df = self._df.withColumn(filed_r, col(struct_t.name).cast(struct_t.dataType))

        return self

    def overwrite_to_dates(self, overwrite_columns: list[tuple[str, str]]) -> 'EasyDF':
        for (column_name, column_date_format) in overwrite_columns:
            if column_date_format:
                self._df = self._df.withColumn(column_name,
                                               to_timestamp(self._df[column_name], column_date_format))
            else:
                self._df = self._df.withColumn(column_name, to_timestamp(self._df[column_name]))

        return self

    def add_audit_fields(self) -> 'EasyDF':
        now_date = datetime.now()
        date_only = now_date.date()
        self._df = self._df.withColumn("CreatedDate", lit(now_date))
        self._df = self._df.withColumn("CreatedYear", lit(now_date.year))
        self._df = self._df.withColumn("CreatedMonth", lit(now_date.month))
        self._df = self._df.withColumn("CreatedDay", lit(now_date.day))
        self._df = self._df.withColumn("CreatedDateOnly", lit(date_only))

        return self

    def remove_audit_fields(self) -> 'EasyDF':
        self.drop_column_if_exists("CreatedDate").drop_column_if_exists("CreatedYear").drop_column_if_exists(
            "CreatedMonth").drop_column_if_exists("CreatedDay").drop_column_if_exists("CreatedDateOnly")

        return self

    def add_hash_column_from_columns(self, hash_column_name: str, column_names: list[str] = None) -> 'EasyDF':
        if not column_names:
            column_names = self._df.columns

        self._df = self._df.withColumn(hash_column_name, sha2(concat_ws("", *column_names), 256))
        return self

    def append_from_dict(self, record: dict) -> 'EasyDF':
        row = Row(**record)
        return self.append_from_row(row)

    def append_from_row(self, row: Row) -> 'EasyDF':
        df = EasyDF._spark.createDataFrame([row], self._df.schema)
        self._df = self.combine_from_df(df, type='union', allowMissingColumns=True)._df
        return self

    def select(self, columns: list[str]) -> 'EasyDF':
        self._df = self._df.select(columns)
        return self

    def select_except(self, columns: list[str]) -> 'EasyDF':
        self._df = self._df.select([col for col in self._df.columns if col not in columns])
        return self

    def clone(self, new_schema: StructType = None) -> 'EasyDF':
        if new_schema:
            new_df = EasyDF._spark.createDataFrame(self._df.rdd, new_schema)
            return EasyDF.create(EasyDF._spark, new_df)
        else:
            return EasyDF.create(EasyDF._spark, self._df)

    def clone_from_pd_df(self, pd_df: DataFramePandas, schema: StructType = None) -> 'EasyDF':
        return EasyDF.create(EasyDF._spark).from_pandas(pd_df, schema)

    def clone_from_list(self, records: list[dict], schema: StructType = None, ignore_order=False) -> 'EasyDF':
        return EasyDF.create(EasyDF._spark).from_list(records, schema, ignore_order)

    def copy(self, new_schema: StructType = None) -> 'EasyDF':
        if new_schema:
            new_df = self._df
            new_df = EasyDeltaHelpers.remove_columns_based_on_schema(new_df, new_schema)
            new_df = EasyDeltaHelpers.add_missing_columns_based_on_schema(new_df, new_schema)
            new_df = EasyDF._spark.createDataFrame(new_df.rdd, new_schema)

            return EasyDF.create(EasyDF._spark, new_df)
        else:
            return EasyDF.create(EasyDF._spark, self._df)

    def distinct(self, columns: list[str] = None) -> 'EasyDF':
        if columns:
            self._df = self._df.distinct(columns)
        else:
            self._df = self._df.distinct()
        return self

    def order_columns(self, columns: list[str]) -> 'EasyDF':
        # Order the columns in the order of the list
        self._df = self._df.select(columns)
        return self

    def add_partitions(self, columns: list[str]) -> 'EasyDF':
        self._df = self._df.repartition(*columns)
        return self

    def is_empty_or_null(self) -> bool:
        return self._df is None or self._df.isEmpty()

    def delete_empty_rows(self, columns: list[str]) -> 'EasyDF':
        self._df = self._df.dropna(subset=columns)
        return self

    def save_from_table_path(self, path: TablePath, df_format="delta", mode="overwrite",
                             merge_option: str = "overwriteSchema", partition_columns: list[str] = None) -> 'EasyDF':
        return self.save_from_path(path.path, df_format, mode, merge_option, partition_columns)

    def save_as_table(self, path: str, df_format="delta", mode="overwrite",
                      merge_option: str = "overwriteSchema", partition_columns: list[str] = None) -> 'EasyDF':
        entry = self._df.write.format(df_format).mode(mode).option(merge_option, "true")

        if partition_columns:
            entry.partitionBy(partition_columns).saveAsTable(path)
        else:
            entry.saveAsTable(path)

        return self

    def save_from_path(self, path: str, df_format="delta", mode="overwrite",
                       merge_option: str = "overwriteSchema", partition_columns: list[str] = None) -> 'EasyDF':
        entry = self._df.write.format(df_format).mode(mode).option(merge_option, "true")

        if partition_columns:
            entry.partitionBy(partition_columns).save(
                path)
        else:
            entry.save(path)
        return self
