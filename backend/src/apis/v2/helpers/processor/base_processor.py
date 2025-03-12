from constants.folder_names import FolderNames
from constants.tf_model import ClassLabel
from core.directory_manager import directory_manager as dm


class BaseProcessor:
    def __init__(self, item: str) -> None:
        self.item = item
        self._initialize_directories()

    def _initialize_directories(self) -> None:
        """Initializes directories for NG, G and Others."""
        base_dir = dm.images_dir / FolderNames.BASE.value / self.item
        self.ng_dir = base_dir / ClassLabel.NG.value
        self.g_dir = base_dir / ClassLabel.G.value
        self.others_dir = base_dir / ClassLabel.OTHERS.value

    def create_directories(self) -> None:
        """Creates necessary directories for evaluation processing."""
        dm.create_directory(self.ng_dir)
        dm.create_directory(self.g_dir)
        dm.create_directory(self.others_dir)
