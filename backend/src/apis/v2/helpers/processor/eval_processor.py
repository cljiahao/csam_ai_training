from constants.folder_names import FolderNames
from constants.image_thresholds import (
    EvalColorsNames,
    EvalThousandsNames,
    EvaluationThreshold,
)
from core.directory_manager import directory_manager as dm


class EvalProcessor:
    def __init__(
        self,
        item: str,
    ) -> None:
        self.item: str = item
        self._initialize_directories()

    def _initialize_directories(self) -> None:
        """Initializes directories for mass production, colors, and thousands sets."""
        eval_dir = dm.images_dir / FolderNames.EVAL.value / self.item
        self.mass_pro_dir = eval_dir / FolderNames.MASS_PRO.value
        self.colors_dir = eval_dir / FolderNames.COLORS.value
        self.thousands_dir = eval_dir / FolderNames.THOUSANDS.value

    def get_mass_pro_count(self) -> None:
        """Counts the number of files in the mass production directory"""
        self.mass_pro_count = len(list(self.mass_pro_dir.iterdir()))

    def get_colors_count(self) -> None:
        """Counts the number of files in each subdirectory under the color directory."""
        self.colors_count = {
            color_folder.name: len(list(color_folder.iterdir()))
            for color_folder in self.colors_dir.iterdir()
        }

    def get_thousands_count(self) -> None:
        """Counts the number of files in each subdirectory under the thousands directory."""
        self.thousands_count = {
            thousands_fol.name: len(list(thousands_fol.iterdir()))
            for thousands_fol in self.thousands_dir.iterdir()
        }

    def increment_mass_pro_count(self, increment: int = 1) -> None:
        """Increments the mass production count in memory."""
        self.mass_pro_count += increment

    def increment_colors_count(self, color_size: str, increment: int = 1) -> None:
        """Increments the count of a specific color in memory."""
        self.colors_count[color_size] = self.colors_count.get(color_size, 0) + increment

    def increment_thousands_count(self, size: str, increment: int = 1) -> None:
        """Increments the count of a specific thousand-set size in memory."""
        self.thousands_count[size] = self.thousands_count.get(size, 0) + increment

    def create_directories(self) -> None:
        """Creates necessary directories for evaluation processing."""
        dm.create_directory(self.mass_pro_dir)

        for color in EvalColorsNames:
            dm.create_directory(self.colors_dir / color.value)

        for thousand in EvalThousandsNames:
            dm.create_directory(self.thousands_dir / thousand.value)

        self.get_mass_pro_count()
        self.get_colors_count()
        self.get_thousands_count()

    def should_save_mass_pro(self) -> bool:
        """Determines if a new mass production image should be saved."""
        return self.mass_pro_count < EvaluationThreshold.MIN_MASS_PRO_SET.value

    def should_save_colors(self, color_size: str) -> bool:
        """Determines if a new colors image should be saved based on threshold."""
        return (
            color_size in self.colors_count
            and self.colors_count[color_size]
            < EvaluationThreshold.MIN_PER_COLORS_SET.value
        )

    def should_save_thousands(self, size: str) -> bool:
        """Determines if a new thousands image should be saved based on threshold."""
        threshold = (
            EvaluationThreshold.MIN_SMALL_THOUSANDS_SET.value
            if size == EvalThousandsNames.SMALL.value
            else EvaluationThreshold.MIN_MEDIUM_BIG_THOUSANDS_SET.value
        )
        return size in self.thousands_count and self.thousands_count[size] < threshold
