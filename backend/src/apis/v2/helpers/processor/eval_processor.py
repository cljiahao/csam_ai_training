from constants.folder_names import FolderNames
from constants.image_thresholds import (
    EvalColorNames,
    EvalThousandNames,
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
        """Initializes directories for mass production, colors, and thousand sets."""
        eval_dir = dm.images_dir / FolderNames.EVAL.value / self.item
        self.mass_pro_dir = eval_dir / FolderNames.MASS_PRO.value
        self.color_dir = eval_dir / FolderNames.COLORS.value
        self.thousand_dir = eval_dir / FolderNames.THOUSANDS.value

    def get_mass_pro_count(self) -> None:
        """Counts the number of files in the mass production directory"""
        self.mass_pro_count = len(list(self.mass_pro_dir.iterdir()))

    def get_color_count(self) -> None:
        """Counts the number of files in each subdirectory under the color directory."""
        self.color_count = {
            color_folder.name: len(list(color_folder.iterdir()))
            for color_folder in self.color_dir.iterdir()
        }

    def get_thousand_count(self) -> None:
        """Counts the number of files in each subdirectory under the thousand directory."""
        self.thousand_count = {
            thousand_fol.name: len(list(thousand_fol.iterdir()))
            for thousand_fol in self.thousand_dir.iterdir()
        }

    def increment_mass_pro_count(self, increment: int = 1) -> None:
        """Increments the mass production count in memory."""
        self.mass_pro_count += increment

    def increment_color_count(self, color_size: str, increment: int = 1) -> None:
        """Increments the count of a specific color in memory."""
        self.color_count[color_size] = self.color_count.get(color_size, 0) + increment

    def increment_thousand_count(self, size: str, increment: int = 1) -> None:
        """Increments the count of a specific thousand-set size in memory."""
        self.thousand_count[size] = self.thousand_count.get(size, 0) + increment

    def create_directories(self) -> None:
        """Creates necessary directories for evaluation processing."""
        dm.create_directory(self.mass_pro_dir)

        for color in EvalColorNames:
            dm.create_directory(self.color_dir / color.value)

        for thousand in EvalThousandNames:
            dm.create_directory(self.thousand_dir / thousand.value)

        self.get_mass_pro_count()
        self.get_color_count()
        self.get_thousand_count()

    def should_save_mass_pro(self) -> bool:
        """Determines if a new mass production image should be saved."""
        return self.mass_pro_count < EvaluationThreshold.MIN_MASS_PRO_SET.value

    def should_save_color(self, color_size: str) -> bool:
        """Determines if a new color image should be saved based on threshold."""
        return (
            color_size in self.color_count
            and self.color_count[color_size]
            < EvaluationThreshold.MIN_PER_COLOR_SET.value
        )

    def should_save_thousand(self, size: str) -> bool:
        """Determines if a new thousand-set image should be saved based on threshold."""
        threshold = (
            EvaluationThreshold.MIN_SMALL_THOUSAND_SET.value
            if size == EvalThousandNames.SMALL.value
            else EvaluationThreshold.MIN_MEDIUM_BIG_THOUSAND_SET.value
        )
        return size in self.thousand_count and self.thousand_count[size] < threshold
