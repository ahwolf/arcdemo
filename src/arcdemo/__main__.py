"""Entry point of the package."""

# %% IMPORTS

from arcdemo import logger
from arcdemo.pipeline.stage_01_data_generation import DataGenerationPipeline
from arcdemo.pipeline.stage_02_data_preparation import DataPreparationPipeline

# %% MAIN

if __name__ == "__main__":
    logger.info("Running the main script.")
    STAGE_NAME = "Data Generation stage"
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = DataGenerationPipeline()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e

    STAGE_NAME = "Data Preparation stage"
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = DataPreparationPipeline()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e
# %%
