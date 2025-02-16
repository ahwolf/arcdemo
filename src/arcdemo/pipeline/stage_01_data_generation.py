from arcdemo import logger
from arcdemo.components.data_generation import DataGeneration
from arcdemo.config.configuration import ConfigurationManager

STAGE_NAME = "Data Generation stage"


class DataGenerationPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        data_generation_config = config.get_data_generation_config()
        data_generation = DataGeneration(config=data_generation_config)
        df = data_generation.save_points()
        logger.info("Saved %d points to %s", len(df), data_generation_config.local_data_file)


if __name__ == "__main__":
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = DataGenerationPipeline()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e
