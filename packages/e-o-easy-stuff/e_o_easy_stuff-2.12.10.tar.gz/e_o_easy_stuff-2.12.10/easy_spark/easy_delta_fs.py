from pyspark.sql import SparkSession
from datetime import datetime
from easy_spark.easy_delta_fs_helpers import EasyDeltaFSHelpers
from easy_spark.easy_hoop_instance import EasyHadoopInstance


class EasyDeltaFS:
    def __init__(self, spark: SparkSession = None, path: str = None, must_java_import=False):
        self.easy_hadoop = EasyHadoopInstance(spark, must_java_import)
        self.easy_delta_fs_helpers = EasyDeltaFSHelpers(spark)
        self.fs_path = None
        self.path: str = path
        self.file_status = None

        if self.path:
            self.from_path(self.path)

    def from_path(self, path: str, is_relative: bool = False) -> 'EasyDeltaFS':
        self.path = path
        self.fs_path = self.easy_delta_fs_helpers.get_fs_path(self.path, is_relative)
        self.init_file_status()
        return self

    def init_file_status(self) -> 'EasyDeltaFS':
        if self.fs_path and self.file_exists():
            self.file_status = self.easy_delta_fs_helpers.get_file_status_from_fs_path(self.fs_path)
        return self

    def file_exists(self) -> bool:
        return self.easy_delta_fs_helpers.file_exists_from_fs_path(self.fs_path)

    def get_file_status(self):
        return self.file_status

    def get_modified_time(self):
        return self.file_status.getModificationTime()

    def get_readable_modified_time(self) -> datetime:
        modified_time = self.get_modified_time()
        return datetime.fromtimestamp(modified_time / 1000.0)

    def get_name(self) -> str:
        return self.file_status.getPath().getName()

    def get_full_path(self) -> str:
        return self.file_status.getPath().toString()

    def delete_file(self) -> bool:
        return self.easy_delta_fs_helpers.delete_file_from_fs_path(self.fs_path)

    def write_file_content(self, content: any, delete_if_exists: bool = False) -> bool:

        if delete_if_exists:
            if self.file_exists():
                self.delete_file()
        elif self.file_exists():
            return False

        output_stream = self.easy_hadoop.fs.create(self.fs_path)
        try:
            output_stream.write(content)
        finally:
            output_stream.close()

        return True
