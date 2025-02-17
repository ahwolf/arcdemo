import geohash
import pandas as pd

from arcdemo.constants import TIME_GAP
from arcdemo.entity.config_entity import DataPreparationConfig
from arcdemo.logger import logger


class DataPreparation:
    """
    Generate a geohash and aggregate by geohash and timestamp.
    """

    def __init__(self, config: DataPreparationConfig):
        self.config = config
        self.df = pd.read_csv(self.config.input_data_file)
        self.geohashed_df = None  # Stores geohashed data
        self.aggregated_df = None  # Stores aggregated data

    def truncate_call_logs(self):
        """
        Read from file and return the last n hours of data.
        Save the data back to that local file.
        """
        now = pd.Timestamp.now()
        self.df["timestamp"] = pd.to_datetime(self.df["timestamp"])
        oldest_valid_value = now - pd.to_timedelta(self.config.history_in_hours, unit="hours")
        self.df = self.df[self.df["timestamp"] >= oldest_valid_value]
        self.df.to_csv(self.config.input_data_file, index=False)

    def geohash_call_logs(self) -> pd.DataFrame:
        """
        Generate a geohash for each datapoint.
        """
        self.geohashed_df = self.df.copy()
        if self.geohashed_df is None:
            raise ValueError("Error: No logs in last 3 hours or call logs is empty")
        self.geohashed_df["geohash"] = self.geohashed_df.apply(
            lambda x: geohash.encode(x["lat"], x["lon"], precision=5), axis=1
        )

    def aggregate_call_logs(self) -> pd.DataFrame:
        """
        Aggregate the data by geohash and timestamp at TIME_GAP intervals.
        """
        if self.geohashed_df is None:
            raise ValueError("Error: Call geohash_call_logs() before aggregate_call_logs()")

        # Ensure timestamp is in datetime format
        df = self.geohashed_df.copy()
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df = df.sort_values(by=["geohash", "timestamp"])
        df.set_index("timestamp", inplace=True)

        # Aggregate data
        self.aggregated_df = (
            df.groupby("geohash")
            .resample(f"{TIME_GAP}s")
            .agg(count=("geohash", "count"))
            .reset_index()
        )

        # Save the aggregated data
        self.aggregated_df.to_csv(self.config.output_data_file, index=False)

    def process_data(self):
        """
        Run the full pipeline: truncate → geohash → aggregate.
        """
        logger.info("Starting data processing pipeline...")
        self.truncate_call_logs()
        logger.info("Truncated call logs...Starting geohashing...")
        self.geohash_call_logs()
        logger.info("Geohashing done...Starting aggregation...")
        self.aggregate_call_logs()
        logger.info("Aggregation done...Data processing pipeline completed.")
