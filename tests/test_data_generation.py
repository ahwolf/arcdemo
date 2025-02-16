import os
import unittest
from unittest.mock import patch

import pandas as pd

from arcdemo.components.data_generation import DataGeneration
from arcdemo.entity.config_entity import DataGenerationConfig


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


if __name__ == "__main__":
    unittest.main()
