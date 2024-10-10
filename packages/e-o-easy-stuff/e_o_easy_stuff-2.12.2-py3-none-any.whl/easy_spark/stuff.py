# class EasyDeltaFSHelper2:
#     @staticmethod
#     def get_file_name_from_path(path: str) -> str:
#         return os.path.basename(path)
#
#     @staticmethod
#     def get_file_extension_from_path(path: str) -> str:
#         return os.path.splitext(path)[1]
#
#     @staticmethod
#     def get_file_name_without_extension(path: str) -> str:
#         return os.path.splitext(os.path.basename(path))[0]
#
#     @staticmethod
#     def get_file_name_and_extension(path: str) -> tuple[str, str]:
#         return os.path.splitext(os.path.basename(path))
#
#     @staticmethod
#     def get_parent_directory(path: str) -> str:
#         return os.path.dirname(path)
#
#     @staticmethod
#     def get_parent_directory_name(path: str) -> str:
#         return os.path.basename(os.path.dirname(path))
#
#     @staticmethod
#     def get_parent_directory_path(path: str) -> str:
#         return os.path.dirname(path)
#
#     @staticmethod
#     def get_parent_directory_name_and_path(path: str) -> tuple[str, str]:
#         return os.path.basename(os.path.dirname(path)), os.path.dirname(path)
#
#     @staticmethod
#     def get_relative_path_from_parent_directory(parent_directory: str, path: str) -> str:
#         return path.replace(parent_directory, "")
#
#     @staticmethod
#     def get_relative_path_from_parent_directory_name(parent_directory_name: str, path: str) -> str:
#         return path.replace(parent_directory_name, "")
#
#     @staticmethod
#     def get_relative_path_from_parent_directory_path(parent_directory_path: str, path: str) -> str:
#         return path.replace(parent_directory_path, "")
#
#     @staticmethod
#     def get_relative_path_from_parent_directory_name_and_path(parent_directory_name: str, parent_directory_path: str,
