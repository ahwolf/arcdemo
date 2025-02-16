from arcdemo.constants import CONFIG_FILE_PATH
from arcdemo.entity.config_entity import BoundingBox, DataGenerationConfig
from arcdemo.utils.common import read_config


class ConfigurationManager:
    def __init__(self, config_filepath=CONFIG_FILE_PATH):
        self.config = read_config(config_filepath)

    def get_data_generation_config(self) -> DataGenerationConfig:
        config = self.config.data_generation

        data_generation_config = DataGenerationConfig(
            number_of_samples=config.number_of_samples,
            local_data_file=config.local_data_file,
            bbox=BoundingBox(
                min_lat=config.bbox.min_lat,
                max_lat=config.bbox.max_lat,
                min_lon=config.bbox.min_lon,
                max_lon=config.bbox.max_lon,
            ),
        )

        return data_generation_config
