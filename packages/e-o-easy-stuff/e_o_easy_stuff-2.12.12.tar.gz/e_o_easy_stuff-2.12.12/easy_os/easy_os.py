import os


class EasyOS:
    @staticmethod
    def get_file_name_from_path(path: str) -> str:
        return os.path.basename(path)

    @staticmethod
    def create_directory(path: str, exist_ok=True) -> None:
        os.makedirs(path, exist_ok=exist_ok)

    @staticmethod
    def create_directory_if_not_exists(path: str) -> None:
        if not os.path.exists(path):
            EasyOS.create_directory(path)

    @staticmethod
    def get_file_extension_from_path(path: str) -> str:
        return os.path.splitext(path)[1]

    @staticmethod
    def get_file_name_without_extension(path: str) -> str:
        return os.path.splitext(os.path.basename(path))[0]

    @staticmethod
    def get_file_name_and_extension(path: str) -> tuple[str, str]:
        return os.path.splitext(os.path.basename(path))

    @staticmethod
    def get_parent_directory(path: str) -> str:
        return os.path.dirname(path)

    @staticmethod
    def get_parent_directory_name(path: str) -> str:
        return os.path.basename(os.path.dirname(path))

    @staticmethod
    def get_parent_directory_path(path: str) -> str:
        return os.path.dirname(path)

    @staticmethod
    def get_parent_directory_name_and_path(path: str) -> tuple[str, str]:
        return os.path.basename(os.path.dirname(path)), os.path.dirname(path)

    @staticmethod
    def get_relative_path_from_parent_directory(parent_directory: str, path: str) -> str:
        return path.replace(parent_directory, "")

    @staticmethod
    def get_relative_path_from_parent_directory_name(parent_directory_name: str, path: str) -> str:
        return path.replace(parent_directory_name, "")

    @staticmethod
    def get_relative_path_from_parent_directory_path(parent_directory_path: str, path: str) -> str:
        return path.replace(parent_directory_path, "")
