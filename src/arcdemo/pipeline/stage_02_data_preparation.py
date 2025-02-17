from arcdemo import logger
from arcdemo.components.data_preparation import DataPreparation
from arcdemo.config.configuration import ConfigurationManager

STAGE_NAME = "Data Preparation stage"


class DataPreparationPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        data_preparation_config = config.get_data_preparation_config()
        data_preparation = DataPreparation(config=data_preparation_config)
        # df = data_preparation.truncate_call_logs()
        # df = data_preparation.geohash_call_logs()
        # df = data_preparation.aggregate_call_logs()
        data_preparation.process_data()

        logger.info(
            "Truncated input data and aggregated %s to %s",
            len(data_preparation.aggregated_df)
            if data_preparation.aggregated_df is not None
            else 0,
            data_preparation_config.output_data_file,
        )


if __name__ == "__main__":
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = DataPreparationPipeline()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e
