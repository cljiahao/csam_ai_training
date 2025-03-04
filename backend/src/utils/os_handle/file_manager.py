import math
from pathlib import Path
import random
from shutil import copyfile, move, rmtree


class FileManager:

    @staticmethod
    def get_file_paths(src_parent_path: Path) -> list[Path]:
        """Returns a list of all .png files in the given directory."""
        if not src_parent_path.exists():
            raise FileNotFoundError(f"Directory not found: {src_parent_path}")

        return list(src_parent_path.glob("*.png"))

    @staticmethod
    def prepare_dst_dir(dst_path: Path, remove: bool = False) -> None:
        """Helper method to ensure the destination directory exists, and remove it if necessary."""
        if remove and dst_path.exists():
            rmtree(dst_path)

        dst_path.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def copy_files_to_dir(
        dst_path: Path, src_file_paths: list[Path], remove: bool = False
    ) -> None:
        """Copy files to the destination directory, with optional removal of the existing destination."""
        FileManager.prepare_dst_dir(dst_path, remove)
        for file_path in src_file_paths:
            copyfile(file_path, dst_path / file_path.name)

    @staticmethod
    def move_files_to_dir(
        dst_path: Path, src_file_paths: list[Path], remove: bool = False
    ) -> None:
        """Move files to the destination directory, with optional removal of the existing destination."""
        FileManager.prepare_dst_dir(dst_path, remove)
        for file_path in src_file_paths:
            move(file_path, dst_path / file_path.name)

    @staticmethod
    def train_val_split(train_dir: Path, val_dir: Path, split: float = 0.2):
        train_file_paths = FileManager.get_file_paths(train_dir)
        split_qty = math.ceil(len(train_file_paths) * split)
        to_move_file_paths = random.sample(train_file_paths, split_qty)
        FileManager.move_files_to_dir(val_dir, to_move_file_paths, True)
