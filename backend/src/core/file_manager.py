import json
from pathlib import Path
from shutil import copyfile, move

from core.directory_manager import directory_manager as dm
from interface.os_handle import FileManagerInterface


class FileManager(FileManagerInterface):
    @staticmethod
    def read_txt(file_path: Path) -> str:
        """Reads content from a text file and returns it as a string."""
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()
        except Exception as e:
            raise IOError(f"Failed to read file {file_path}: {e}")

    @staticmethod
    def write_txt(file_path: Path, content: str) -> None:
        """Writes content to a text file, creating the file if it doesn't exist."""
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(content)
        except Exception as e:
            raise IOError(f"Failed to write to file {file_path}: {e}")

    @staticmethod
    def read_json(file_path: Path) -> dict[str, any]:
        """Reads a JSON file and returns its content as a dictionary."""
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to decode JSON from file {file_path}: {e}")
        except Exception as e:
            raise IOError(f"Failed to read JSON file {file_path}: {e}")

    @staticmethod
    def write_json(file_path: Path, content: dict) -> None:
        """Writes a dictionary to a JSON file, creating the file if it doesn't exist."""
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(content, file, indent=4)
        except Exception as e:
            raise IOError(f"Failed to write JSON to file {file_path}: {e}")

    @staticmethod
    def copy_files_to_dir(
        dst_path: Path, src_file_paths: list[Path], remove: bool = False
    ) -> None:
        """Copy files to the destination directory, with optional removal of the existing destination."""
        dm.create_directory(dst_path, remove)
        for file_path in src_file_paths:
            copyfile(file_path, dst_path / file_path.name)

    @staticmethod
    def move_files_to_dir(
        dst_path: Path, src_file_paths: list[Path], remove: bool = False
    ) -> None:
        """Move files to the destination directory, with optional removal of the existing destination."""
        dm.create_directory(dst_path, remove)
        for file_path in src_file_paths:
            move(file_path, dst_path / file_path.name)
