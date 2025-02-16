from dataclasses import dataclass
from pathlib import Path


@dataclass
class BoundingBox:
    min_lat: float
    max_lat: float
    min_lon: float
    max_lon: float


@dataclass(frozen=True)
class DataGenerationConfig:
    number_of_samples: int
    local_data_file: Path
    bbox: BoundingBox


@dataclass
class DataPreparationConfig:
    input_data_file: str
    history_in_hours: int
    output_data_file: str
