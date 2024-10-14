from pyspark.sql import SparkSession
from easy_spark.easy_df import EasyDF
from easy_utils.easy_singleton import easy_singleton


@easy_singleton
class EasySparkInstance:

    def __init__(self, spark: SparkSession = None):
        if spark:
            self._spark = spark
        pass

    @property
    def spark(self) -> SparkSession:
        return self._spark

    def new_easy_df(self, df=None) -> EasyDF:
        return EasyDF.create(self.spark, df)
