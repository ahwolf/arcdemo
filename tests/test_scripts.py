import os
import unittest
from unittest.mock import patch

import numpy as np
import pandas as pd

from arcdemo.components.data_generation import DataGeneration
from arcdemo.components.data_preparation import DataPreparation
from arcdemo.entity.config_entity import DataGenerationConfig, DataPreparationConfig


class TestDataGeneration(unittest.TestCase):
    """Test cases for DataGeneration class."""

    def setUp(self):
        """Setup configuration for DataGeneration tests."""
        self.config = DataGenerationConfig(
            number_of_samples=5,
            bbox=type("BBox", (), {"min_lat": 10, "max_lat": 20, "min_lon": 30, "max_lon": 40}),
            local_data_file="test_generated_data.csv",
        )
        self.data_generator = DataGeneration(self.config)

    @patch("pandas.Timestamp.now")
    def test_generate_timestamps(self, mock_now):
        """Test if generated timestamps are within TIME_GAP seconds from the current time."""
        mock_now.return_value = pd.Timestamp("2024-02-16 12:00:00")
        timestamps = self.data_generator._generate_timestamps()
        self.assertEqual(len(timestamps), self.config.number_of_samples)
        self.assertTrue((mock_now.return_value - timestamps).max().seconds <= 900)

    def test_generate_points(self):
        """Test if generated points fall within the bounding box."""
        points = self.data_generator._generate_points()
        self.assertEqual(len(points), self.config.number_of_samples)
        self.assertTrue((points["lat"] >= self.config.bbox.min_lat).all())
        self.assertTrue((points["lat"] <= self.config.bbox.max_lat).all())
        self.assertTrue((points["lon"] >= self.config.bbox.min_lon).all())
        self.assertTrue((points["lon"] <= self.config.bbox.max_lon).all())

    def test_save_points(self):
        """Test if points are saved correctly to a CSV file."""
        points = self.data_generator.save_points()
        self.assertTrue(os.path.exists(self.config.local_data_file))
        saved_data = pd.read_csv(self.config.local_data_file, names=["lat", "lon", "timestamp"])
        self.assertEqual(len(saved_data), len(points))

    def tearDown(self):
        """Clean up generated test files."""
        if os.path.exists(self.config.local_data_file):
            os.remove(self.config.local_data_file)


class TestDataPreparation(unittest.TestCase):
    """Test cases for DataPreparation class."""

    def setUp(self):
        """Setup configuration and sample data for DataPreparation tests."""
        self.config = DataPreparationConfig(
            input_data_file="test_input_data.csv",
            output_data_file="test_output_data.csv",
            history_in_hours=24,
        )

        # Sample data
        data = {
            "timestamp": pd.date_range(start="2024-02-15 12:00:00", periods=5, freq="H"),
            "lat": np.random.uniform(10, 20, 5),
            "lon": np.random.uniform(30, 40, 5),
        }
        self.df = pd.DataFrame(data)

        # Save to test file
        self.df.to_csv(self.config.input_data_file, index=False)

        # Initialize DataPreparation instance
        self.data_preparation = DataPreparation(self.config)

    def test_truncate_call_logs(self):
        """Test truncating call logs to keep only the last `history_in_hours` hours."""
        self.data_preparation.truncate_call_logs()
        truncated_df = self.data_preparation.df
        now = pd.Timestamp.now()
        oldest_valid_time = now - pd.Timedelta(hours=self.config.history_in_hours)
        self.assertTrue((truncated_df["timestamp"] >= oldest_valid_time).all())

    def test_geohash_call_logs(self):
        """Test if geohashes are correctly generated."""
        self.data_preparation.geohash_call_logs()
        self.assertIn("geohash", self.data_preparation.geohashed_df.columns)
        self.assertTrue(self.data_preparation.geohashed_df["geohash"].notnull().all())

    def test_aggregate_call_logs(self):
        """Test if aggregation by geohash and timestamp works."""
        self.data_preparation.geohash_call_logs()
        self.data_preparation.aggregate_call_logs()
        aggregated_df = self.data_preparation.aggregated_df
        self.assertIn("count", aggregated_df.columns)
        self.assertGreaterEqual(aggregated_df["count"].sum(), 1)

    def tearDown(self):
        """Clean up test files."""
        if os.path.exists(self.config.input_data_file):
            os.remove(self.config.input_data_file)
        if os.path.exists(self.config.output_data_file):
            os.remove(self.config.output_data_file)


if __name__ == "__main__":
    unittest.main()
