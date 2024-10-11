from easy_spark.easy_hoop_instance import EasyHadoopInstance
from easy_utils.easy_singleton import easy_singleton
from datetime import datetime
from typing import Generator, Iterator


class EasyFileDetails:
    def __init__(self, fs_path, file_status, is_directory: bool, file_name: str, full_path: str,
                 readable_modified_time: datetime):
        self.fs_path = fs_path
        self.file_status = file_status
        self.file_name: str = file_name
        self.full_path: str = full_path
        self.readable_modified_time: datetime = readable_modified_time
        self.is_directory: bool = is_directory


@easy_singleton
class EasyDeltaFSHelpers:
    def __init__(self, spark):
        self.easy_hadoop = EasyHadoopInstance(spark, True)

    def get_fs_path_from_status(self, status):
        return status.getPath()

    def get_file_name_from_status(self, status) -> str:
        return status.getPath().getName()

    def get_file_full_path_from_status(self, status) -> str:
        return status.getPath().toString()

    def get_file_modification_time_from_status(self, status):
        return status.getModificationTime()

    def get_readable_file_modification_time_from_status(self, status) -> datetime:
        return datetime.fromtimestamp(self.get_file_modification_time_from_status(status) / 1000.0)

    def is_directory_from_status(self, status) -> bool:
        return status.isDirectory()

    def delete_file_from_fs_path(self, fs_path) -> bool:
        return self.easy_hadoop.fs.delete(fs_path, True)

    def file_exists_from_fs_path(self, fs_path) -> bool:
        return self.easy_hadoop.fs.exists(fs_path)

    def file_exists_from_path(self, path: str, is_relative: bool) -> bool:
        fs_path = self.get_fs_path(path, is_relative)
        return self.file_exists_from_fs_path(fs_path)

    def get_file_status_from_fs_path(self, fs_path):
        return self.easy_hadoop.fs.getFileStatus(fs_path)

    def get_file_status_from_path(self, path: str, is_relative: bool):
        fs_path = self.get_fs_path(path, is_relative)
        return self.get_file_status_from_fs_path(fs_path)

    def get_fs_path(self, path: str, is_relative: bool):
        if is_relative:
            return self.get_fs_absolute_path(path)
        else:
            return self.easy_hadoop.make_path(path)

    def get_fs_absolute_path(self, relative_path: str):
        fs_path = self.easy_hadoop.make_path(relative_path)
        return fs_path.makeQualified(self.easy_hadoop.fs.getUri(),
                                     self.easy_hadoop.fs.getWorkingDirectory())

    def list_statuses_from_fs_path(self, fs_path) -> list:
        return list(self.easy_hadoop.fs.listStatus(fs_path))

    def list_statuses_from_path(self, path: str, is_relative: bool) -> list:
        fs_path = self.get_fs_path(path, is_relative)
        return self.list_statuses_from_fs_path(fs_path)

    def get_file_details_from_status(self, status) -> EasyFileDetails:
        is_directory = self.is_directory_from_status(status)
        file_name = self.get_file_name_from_status(status)
        fs_path = self.get_fs_path_from_status(status)
        full_path = self.get_file_full_path_from_status(status)

        if is_directory:
            return EasyFileDetails(fs_path, status, is_directory, file_name, full_path, None)

        readable_modified_time = self.get_readable_file_modification_time_from_status(status)

        return EasyFileDetails(fs_path, status, is_directory, file_name, full_path, readable_modified_time)

    def get_file_details_from_fs_path(self, fs_path) -> EasyFileDetails:
        status = self.get_file_status_from_fs_path(fs_path)
        return self.get_file_details_from_status(status)

    def get_file_details_from_path(self, path: str, is_relative: bool) -> EasyFileDetails:
        fs_path = self.get_fs_path(path, is_relative)
        return self.get_file_details_from_fs_path(fs_path)

    def list_path_details_from_fs_path(self, fs_path) -> Iterator[EasyFileDetails]:
        statuses = self.list_statuses_from_fs_path(fs_path)
        for status in statuses:
            yield self.get_file_details_from_status(status)

    def list_path_details_from_path(self, path: str, is_relative: bool) -> Iterator[EasyFileDetails]:
        fs_path = self.get_fs_path(path, is_relative)
        return self.list_path_details_from_fs_path(fs_path)
