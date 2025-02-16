# Description: Generate random points within a bounding box.
import numpy as np
import pandas as pd

from arcdemo.constants import TIME_GAP
from arcdemo.entity.config_entity import DataGenerationConfig


class DataGeneration:
    """
    Generate random points within a bounding box.
    """

    def __init__(self, config: DataGenerationConfig):
        self.config = config

    def _generate_timestamps(self) -> pd.Series:
        """
        Generate n random timestamps within the last TIME_GAP seconds.
        """
        # generate n random integers between 0 and 15*60
        seconds = np.random.randint(0, TIME_GAP, self.config.number_of_samples)
        # subtract the seconds from the current time
        now = pd.Timestamp.now()
        timestamps = now - pd.to_timedelta(seconds, unit="s")
        return timestamps

    def _generate_points(self) -> pd.DataFrame:
        """
        Generate n random points within the bounding box.
        """
        n = self.config.number_of_samples
        bbox = self.config.bbox
        lats = np.random.uniform(bbox.min_lat, bbox.max_lat, n)
        lons = np.random.uniform(bbox.min_lon, bbox.max_lon, n)
        timestamps = self._generate_timestamps()
        return pd.DataFrame(
            {
                "lat": lats,
                "lon": lons,
                "timestamp": timestamps,
            }
        )

    def save_points(self) -> pd.DataFrame:
        """
        Save the generated points to a local file.
        """
        points = self._generate_points()
        points.to_csv(self.config.local_data_file, index=False, mode="a", header=False)
        return points
