from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from easy_spark.easy_delta import EasyDeltaPath
from easy_spark.easy_df import EasyDF
from py4j.java_gateway import java_import

from easy_spark_fs.easy_spark_fs import EasySparkFS


def easy_create_container(spark: SparkSession, must_java_import=False) -> tuple[
    Callable[[DataFrame | None], EasyDF], Callable[[str, bool, StructType, bool], EasyDeltaPath], Callable[
        [str], EasySparkFS]]:
    _spark = spark

    if must_java_import:
        java_import(_spark._jvm, 'org.apache.hadoop.fs.FileSystem')
        java_import(_spark._jvm, 'org.apache.hadoop.conf.Configuration')
        java_import(_spark._jvm, 'org.apache.hadoop.fs.Path')

    def create_easy_df(df: DataFrame = None):
        return EasyDF(df, _spark)

    def create_easy_delta(path: str, create_table_if_not_exists: bool = False, create_schema: StructType = None,
                          init_delta: bool = True):
        return EasyDeltaPath(path, _spark, create_table_if_not_exists, create_schema, init_delta)

    def create_easy_delta_fs(path: str):
        return EasySparkFS(_spark, path)

    return (
        create_easy_df,
        create_easy_delta,
        create_easy_delta_fs
    )
