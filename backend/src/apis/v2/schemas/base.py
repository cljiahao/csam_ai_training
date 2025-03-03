from enum import Enum


class ServerMode(str, Enum):
    cai = "CAI"
    cdc = "CDC"


class SettingsMode(str, Enum):
    batch = "Batch"
    chip = "Chip"
