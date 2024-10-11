from pyspark.sql import SparkSession
from easy_spark.easy_delta_fs import EasyDeltaFS
from easy_spark.easy_delta_helpers import EasyDeltaHelpers
from easy_spark.easy_df import EasyDF
from easy_spark.easy_spark_instance import EasySparkInstance
from easy_spark.table_path import TablePath
from pyspark.sql.functions import *
from delta.tables import *
from pyspark.sql import Row
from pandas import DataFrame as DataFramePandas
import pandas as pd


# TODO: Add Enums
# TODO: Use with
# TODO: Add Z Index and optimize
# TODO: Add Other optomize
# TODO: unprocessed_df = df_with_filename.filter(~col("FileName").isin(processed_files))
# TODO: df.write.mode("overwrite").parquet("abfss://58ab9357-aa57-4436-a7b6-98d03b217e80@onelake.dfs.fabric.microsoft.com/95f79cfd-4da0-4cc5-8411-6cf8d5def499/Files/Staging/Test")
# TODO: Save as Table
# TODO: Partisions
# TODO: Add join stuff
# TODO: Check how to use FS better in delta table
# TODO: Fs wont wort for relative path for example to table
# TODO: Rather use spark.catalog.tableExists('SportRadar_LH.SportRadar_Spend')
# TODO: Add create to FS
# TODO: To know if object actually created
# TODO: FS Should be better with FS stuff
# TODO: Add filter by builder
# TODO: Check how many times is EasyDF is used
# TODO: Check how times this is used EasyDF.create
# TODO: coloumns Fix
# TODO: Fix all names of clases
# TODO: Make all apis to support the new Condition value
# TODO: Move some of the static stuff out
# TODO Use Partioning everywhere you can
# TODO Add Method to remove nulls from df
# TODO: On SAving, do you need to pass the path, can you maybe get it from the object
# TODO: When you pass in None for dateformat , it does not work
# TODO: os.path.exists and os.mkdir(path)
# TODO: TargetTable_Exists = spark.catalog.tableExists(TargetFullTableName)
# TODO: Also support group of operators
# TODO: More SQL queries like delete, join
# TODO: Complete OS
# TODO: Update EasyDeltaFS to use all helpers methods
# TODO: USE helpers in delta like FS
# TODO: Do the insert
# TODO: Check all the imports
# TODO: Rename by single column name
# TODO: Nothing should throw an error
# TODO: Static method create from TablePath
# TODO: For merge you can specify what records you want to insert
# TODO: Overwrite eq and + -
# TODO:
# filtered_df = easy_df.df.filter(
#             (col('LastImpression').isNull()) |  # Filters None values
#             (col('LastImpression') == '') |  # Filters empty strings
#             (isnan(col('LastImpression')))  # Filters NaN values
#         )

# @staticmethod
#     def _get_all_directories(path: str) -> list[str]:
#         sc = spark.sparkContext
#         hadoop_conf = sc._jsc.hadoopConfiguration()
#         fs = sc._jvm.org.apache.hadoop.fs.FileSystem.get(hadoop_conf)
#         Path = sc._jvm.org.apache.hadoop.fs.Path
#
#         path_obj = Path(path)
#         dirs = []
#         queue = [path_obj]
#
#         while queue:
#             current_path = queue.pop(0)
#             try:
#                 # List the status of files/directories in the current path
#                 files_status = fs.listStatus(current_path)
#                 for file_status in files_status:
#                     if file_status.isDirectory():
#                         dir_path = file_status.getPath().toString()
#                         dirs.append(dir_path)
#                         queue.append(file_status.getPath())
#             except Exception as e:
#                 print(f"Error accessing {current_path}: {e}", file=sys.stderr)
#                 continue
#         return dirs


# import os
# from py4j.java_gateway import java_import
#
# java_import(sc._jvm, 'org.apache.hadoop.fs.*')
#
# sc = spark.sparkContext
# hadoop_conf = sc._jsc.hadoopConfiguration()
# fs = sc._jvm.org.apache.hadoop.fs.FileSystem.get(hadoop_conf)
# Path = sc._jvm.org.apache.hadoop.fs.Path
#
#
# #relative_path = '/fc5d7988-042f-48c7-88cb-9f82a32c3ea3/Files/Staging/2024/9'
# relative_path = 'Files/Staging/2024/9'
#
# path_relative = sc._jvm.Path(relative_path)
# absolute_path = path_relative.makeQualified(fs.getUri(), fs.getWorkingDirectory())
# print(absolute_path)
#
# #path_obj = Path('/lakehouse/default/Files/Staging/2024/9')
# file_status = fs.listStatus(absolute_path)
# display(list(file_status))
# for file in file_status:


class EasyDeltaPath:
    _spark: SparkSession = None

    def __init__(self, path: str = None, spark: SparkSession = None, create_table_if_not_exists: bool = False,
                 create_schema: StructType = None, init_delta: bool = True, for_name=False,
                 partition_columns: list[str] = None):
        self.spark_instance = EasySparkInstance(spark)
        EasyDeltaPath._spark = spark
        self._delta_path = None
        self.path: str = path
        self.for_name: bool = for_name

        if EasyDeltaPath._spark and self.path:
            if for_name:
                self.for_name_from_path(self.path, False)
            else:
                self.from_path(self.path, False)

            if create_table_if_not_exists:
                self.create_empty_if_not_exists(create_schema, init_delta=init_delta,
                                                partition_columns=partition_columns)
            elif init_delta:
                self.init_delta()

    @staticmethod
    def create(spark: SparkSession, path: str = None, create_schema: StructType = None, init_delta: bool = True,
               partition_columns: list[str] = None):

        create_table_if_not_exists = True if create_schema else False
        return EasyDeltaPath(path, spark, create_table_if_not_exists, create_schema, init_delta,
                             partition_columns=partition_columns)

    @staticmethod
    def create_for_name(spark: SparkSession, path: str = None, create_schema: StructType = None,
                        init_delta: bool = True, partition_columns: list[str] = None):

        create_table_if_not_exists = True if create_schema else False
        return EasyDeltaPath(path, spark, create_table_if_not_exists, create_schema, init_delta, True,
                             partition_columns)

    @staticmethod
    def create_for_name_from_lh_table(spark: SparkSession, lh_name: str, table_name: str,
                                      create_schema: StructType = None,
                                      init_delta: bool = True, partition_columns: list[str] = None):
        path = f'{lh_name}.{table_name}'
        return EasyDeltaPath.create_for_name(spark, path, create_schema, init_delta, partition_columns)

    @staticmethod
    def create_from_lh_table(spark: SparkSession, lh_name: str, table_name: str,
                             create_schema: StructType = None,
                             init_delta: bool = True, partition_columns: list[str] = None):
        return EasyDeltaPath.create_for_name_from_lh_table(spark, lh_name, table_name, create_schema, init_delta,
                                                           partition_columns)

    @property
    def delta_path(self):
        return self._delta_path

    def to_easy_df(self) -> EasyDF:
        return EasyDF(self._delta_path.toDF(), EasyDeltaPath._spark)

    def to_fs(self, must_java_import=False) -> EasyDeltaFS:
        return EasyDeltaFS(EasyDeltaPath._spark, self.path, must_java_import)

    @staticmethod
    def table_exists(table_name: str, db_name: str) -> bool:
        return EasyDeltaPath._spark.catalog._jcatalog.tableExists(table_name, db_name)

    @staticmethod
    def table_exists_from_full_path(full_path: str) -> bool:
        return EasyDeltaPath._spark.catalog._jcatalog.tableExists(full_path)

    @staticmethod
    def file_exists(path: str, must_java_import=False) -> bool:
        return EasyDeltaFS(EasyDeltaPath._spark, path, must_java_import).file_exists()

    def from_path(self, path: str, init_delta: bool = True) -> 'EasyDeltaPath':
        self.path = path

        if init_delta:
            self.init_delta()

        return self

    def from_table_path(self, path: TablePath, init_delta: bool = True) -> 'EasyDeltaPath':
        return self.from_path(path.path, init_delta)

    def for_name_from_path(self, path: str, init_delta: bool = True) -> 'EasyDeltaPath':
        self.path = path
        self.for_name = True

        if init_delta:
            self.init_delta()

        return self

    def for_name_from_lh_table(self, lh_name: str, table_name: str, init_delta: bool = True) -> 'EasyDeltaPath':
        path = f'{lh_name}.{table_name}'

        return self.for_name_from_path(path, init_delta)

    def init_delta(self, throw_when_fail=True) -> 'EasyDeltaPath':
        if self.for_name:
            self._delta_path = DeltaTable.forName(EasyDeltaPath._spark, self.path)
        else:
            self._delta_path = DeltaTable.forPath(EasyDeltaPath._spark, self.path)

        return self

    def create_empty_if_not_exists(self, schema: StructType = None, df_format="delta",
                                   init_delta: bool = False, partition_columns: list[str] = None) -> 'EasyDeltaPath':
        if self.for_name:
            if not EasyDeltaPath.table_exists_from_full_path(self.path):
                self.create_empty(schema, df_format, partition_columns)
        elif not EasyDeltaPath.file_exists(self.path):
            self.create_empty(schema, df_format, partition_columns)

        if init_delta and self._delta_path is None:
            self.init_delta()

        return self

    def create_empty(self, schema: StructType = None, df_format="delta",
                     partition_columns: list[str] = None) -> 'EasyDeltaPath':
        easy_df = EasyDF.create(EasyDeltaPath._spark).empty(schema)

        self.save(easy_df, df_format, partition_columns=partition_columns)
        return self

    def get_dict(self, keys: dict[str, any]) -> dict[str, any] | None:
        df = self.to_easy_df().filter(keys).df
        if df is None or df.count() == 0:
            return None

        rows = df.collect()
        return rows[0].asDict()

    def get_dict_using_filter(self, keys: dict[str, any]) -> dict[str, any] | None:
        df = self.to_easy_df().filter_using_filter(keys).df
        if df is None or df.count() == 0:
            return None

        rows = df.collect()
        return rows[0].asDict()

    def get_dict_by_filter(self, condition: str) -> dict[str, any] | None:
        df = self.to_easy_df().filter_by_filter(condition).df
        if df is None or df.count() == 0:
            return None

        rows = df.collect()
        return rows[0].asDict()

    def get_dict_by_where(self, condition: str) -> dict[str, any] | None:
        df = self.to_easy_df().where(condition).df
        if df is None or df.count() == 0:
            return None

        rows = df.collect()
        return rows[0].asDict()

    def get_rows_using_filter(self, keys: dict[str, any] = None) -> list[Row]:
        return self.to_easy_df().filter_using_filter(keys).df.collect()

    def get_rows_by_filter(self, condition: str = None) -> list[Row]:
        return self.to_easy_df().filter_by_filter(condition).df.collect()

    def get_rows_by_where(self, condition: str = None) -> list[Row]:
        return self.to_easy_df().where(condition).df.collect()

    def get_rows_using_where(self, keys: dict[str, any] = None) -> list[Row]:
        return self.to_easy_df().where_using_where(keys).df.collect()

    def get_rows(self, keys: dict[str, any] = None) -> list[Row]:
        return self.to_easy_df().filter(keys).df.collect()

    def get_list(self, keys: dict[str, any] = None) -> list[dict[str, any]]:
        rows = self.get_rows(keys)
        return [row.asDict() for row in rows]

    def get_list_using_filter(self, keys: dict[str, any] = None) -> list[dict[str, any]]:
        rows = self.get_rows_using_filter(keys)
        return [row.asDict() for row in rows]

    def get_list_by_filter(self, condition: str = None) -> list[dict[str, any]]:
        rows = self.get_rows_by_filter(condition)
        return [row.asDict() for row in rows]

    def get_list_by_where(self, condition: str = None) -> list[dict[str, any]]:
        rows = self.get_rows_by_where(condition)
        return [row.asDict() for row in rows]

    def add_from_dict(self, record: dict, df_format="delta", schema: StructType = None) -> 'EasyDeltaPath':
        return self.add_from_list([record], df_format, schema)

    def add_from_list(self, records: list[dict], df_format="delta",
                      schema: StructType = None, ignore_order=False) -> 'EasyDeltaPath':
        new_easy_df = self.spark_instance.new_easy_df().clone_from_list(records, schema, ignore_order)
        self.save(new_easy_df, df_format, mode="append")
        return self

    def add_from_df(self, df: DataFrame, df_format="delta", merge_option: str = "overwriteSchema",
                    partition_columns: list[str] = None) -> 'EasyDeltaPath':
        new_easy_df = self.spark_instance.new_easy_df(df)
        self.save(new_easy_df, df_format, mode="append", merge_option=merge_option, partition_columns=partition_columns)
        return self

    def combine_from_df(self, df: DataFrame, df_format="delta", type: str = 'unionByName',
                        allowMissingColumns: bool = True, merge_option: str = "overwriteSchema",
                        partition_columns: list[str] = None) -> 'EasyDeltaPath':
        easy_df = self.to_easy_df()
        easy_df.combine_from_df(df, type, allowMissingColumns)
        self.save(easy_df, df_format, merge_option=merge_option, partition_columns=partition_columns)
        return self

    def add_from_pd_df(self, pd_df: DataFramePandas, df_format="delta", schema: StructType = None,
                       merge_option: str = "overwriteSchema", partition_columns: list[str] = None) -> 'EasyDeltaPath':
        new_easy_df = self.spark_instance.new_easy_df().clone_from_pd_df(pd_df, schema)
        self.save(new_easy_df, df_format, mode="append", merge_option=merge_option, partition_columns=partition_columns)
        return self

    def combine_from_pd_df(self, pd_df: DataFramePandas, df_format="delta", schema: StructType = None,
                           type: str = 'unionByName',
                           allowMissingColumns: bool = True, merge_option: str = "overwriteSchema") -> 'EasyDeltaPath':
        easy_df = self.to_easy_df()
        easy_df.combine_from_pd_df(pd_df, schema, type, allowMissingColumns)
        self.save(easy_df, df_format, merge_option=merge_option)
        return self

    def update(self, keys: dict[str, any], values: dict[str, any]) -> 'EasyDeltaPath':
        conditions = EasyDeltaPath._build_condition(keys)
        sets = {k: lit(v) for k, v in values.items()}

        self._delta_path.update(
            condition=conditions,
            set=sets
        )
        return self

    def update_by_condition(self, condition: str, values: dict[str, any]) -> 'EasyDeltaPath':
        sets = {k: lit(v) for k, v in values.items()}
        self._delta_path.update(
            condition=condition,
            set=sets
        )
        return self

    def delete(self, keys: dict[str, any] = None,
               multiple_keys: list[tuple[str, list]] = None) -> 'EasyDeltaPath':
        conditions = ""

        if keys:
            conditions = EasyDeltaPath._build_condition(keys)

        if multiple_keys and len(multiple_keys) > 0:
            conditions = EasyDeltaHelpers.build_condition_by_multiple_keys(multiple_keys, conditions)

        self._delta_path.delete(condition=conditions)
        return self

    def delete_by_multiple_keys(self, key: str, key_values: list) -> 'EasyDeltaPath':
        self._delta_path.delete(f"{key} in {tuple(key_values)}")
        return self

    def delete_by_condition(self, condition: str) -> 'EasyDeltaPath':
        self._delta_path.delete(condition)
        return self

    def delete_all(self, df_format="delta") -> 'EasyDeltaPath':
        easy_df = self.to_easy_df()
        easy_df.clear()
        self.save(easy_df, df_format, mode="overwrite")

        return self

    def save(self, easy_df: EasyDF = None, df_format="delta", mode="overwrite",
             merge_option: str = "overwriteSchema", partition_columns: list[str] = None) -> 'EasyDeltaPath':
        if not easy_df:
            easy_df = self.to_easy_df()

        if self.for_name:
            easy_df.save_as_table(self.path, df_format=df_format, mode=mode, merge_option=merge_option,
                                  partition_columns=partition_columns)
        else:
            easy_df.save_from_path(self.path, df_format=df_format, mode=mode, merge_option=merge_option,
                                   partition_columns=partition_columns)

        return self

    def merge_from_list(self, keys: list[str], records: list[dict], schema: StructType = None,
                        add_missing_coloumns=True, add_missing_coloumns_to_current=False, df_format="delta",
                        ignore_order=False, to_keys: dict[str, any] = None) -> 'EasyDeltaPath':

        if schema is None:
            easy_df = self.to_easy_df()
            schema = easy_df.current_schema

        if ignore_order:
            rows = [Row(**record) for record in records]
            df = EasyDeltaPath._spark.createDataFrame(rows, schema)
        else:
            pdf_df = pd.DataFrame(records)
            df = EasyDeltaPath._spark.createDataFrame(pdf_df, schema)

        return self.merge_from_df(keys, df, add_missing_coloumns, add_missing_coloumns_to_current, df_format, to_keys)

    def merge_from_tuple(self, keys: list[str], records: list[tuple], schema: StructType = None,
                         add_missing_coloumns=True, add_missing_coloumns_to_current=False,
                         df_format="delta", to_keys: dict[str, any] = None) -> 'EasyDeltaPath':
        if schema is None:
            easy_df = self.to_easy_df()
            schema = easy_df.current_schema

        df = EasyDeltaPath._spark.createDataFrame(records, schema)
        return self.merge_from_df(keys, df, add_missing_coloumns, add_missing_coloumns_to_current, df_format, to_keys)

    def merge_from_df(self, keys: list[str], df: DataFrame, add_missing_coloumns=True,
                      add_missing_coloumns_to_current=False, df_format="delta",
                      to_keys: dict[str, any] = None) -> 'EasyDeltaPath':
        current_df = self._delta_path.toDF()
        df_columns = df.columns
        current_columns = current_df.columns

        if add_missing_coloumns:
            for current_column in current_columns:
                if current_column not in df_columns:
                    df = df.withColumn(current_column, lit(None).cast(current_df.schema[current_column].dataType))

        if add_missing_coloumns_to_current:
            current_df_has_new_columns = False
            for df_column in df_columns:
                if df_column not in current_columns:
                    current_df = current_df.withColumn(df_column, lit(None).cast(df.schema[df_column].dataType))
                    current_df_has_new_columns = True

            if current_df_has_new_columns:
                # TODO: Fix this
                EasyDF(current_df, EasyDeltaPath._spark).save_from_path(self.path, df_format=df_format,
                                                                        mode="overwrite",
                                                                        merge_option="overwriteSchema")

                # TODO: Fix this
                self._delta_path = DeltaTable.forPath(EasyDeltaPath._spark, self.path)

        merge_relationships = [f"A.`{key}` = B.`{key}` and " for key in keys]
        merge_relationships = "".join(merge_relationships)[:-4]

        if to_keys:
            to_conditions = EasyDeltaHelpers.build_condition(to_keys, "", "A")
            merge_relationships += f"And {to_conditions}"

        self._delta_path.alias('A').merge(
            df.alias('B'),
            merge_relationships
        ).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()

        return self

    # Private Method
    @staticmethod
    def _build_condition(keys: dict[str, any]):
        return EasyDeltaHelpers.build_condition(keys)
