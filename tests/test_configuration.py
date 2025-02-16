"""Configuration for the tests."""

import unittest
from unittest.mock import MagicMock, patch

from arcdemo.config.configuration import ConfigurationManager
from arcdemo.entity.config_entity import BoundingBox, DataGenerationConfig, DataPreparationConfig


class TestConfigurationManager(unittest.TestCase):
    def setUp(self):
        """Mock configuration for testing."""
        self.mock_config = MagicMock()
        self.mock_config.data_generation.number_of_samples = 100
        self.mock_config.data_generation.local_data_file = "test_data.csv"
        self.mock_config.data_generation.bbox.min_lat = 10.0
        self.mock_config.data_generation.bbox.max_lat = 20.0
        self.mock_config.data_generation.bbox.min_lon = 30.0
        self.mock_config.data_generation.bbox.max_lon = 40.0

        self.mock_config.data_preparation.input_data_file = "test_input.csv"
        self.mock_config.data_preparation.history_in_hours = 24
        self.mock_config.data_preparation.output_data_file = "test_output.csv"

    @patch("arcdemo.config.configuration.read_config")
    def test_get_data_generation_config(self, mock_read_config):
        """Test if data generation config is loaded correctly."""
        mock_read_config.return_value = self.mock_config
        config_manager = ConfigurationManager()

        data_gen_config = config_manager.get_data_generation_config()
        self.assertIsInstance(data_gen_config, DataGenerationConfig)
        self.assertEqual(data_gen_config.number_of_samples, 100)
        self.assertEqual(data_gen_config.local_data_file, "test_data.csv")
        self.assertIsInstance(data_gen_config.bbox, BoundingBox)
        self.assertEqual(data_gen_config.bbox.min_lat, 10.0)
        self.assertEqual(data_gen_config.bbox.max_lat, 20.0)

    @patch("arcdemo.config.configuration.read_config")
    def test_get_data_preparation_config(self, mock_read_config):
        """Test if data preparation config is loaded correctly."""
        mock_read_config.return_value = self.mock_config
        config_manager = ConfigurationManager()

        data_prep_config = config_manager.get_data_preparation_config()
        self.assertIsInstance(data_prep_config, DataPreparationConfig)
        self.assertEqual(data_prep_config.input_data_file, "test_input.csv")
        self.assertEqual(data_prep_config.history_in_hours, 24)
        self.assertEqual(data_prep_config.output_data_file, "test_output.csv")

    @patch("arcdemo.config.configuration.read_config")
    def test_missing_configuration(self, mock_read_config):
        """Test if an exception is raised when a required field is missing."""
        # Simulate missing fields in the config
        mock_incomplete_config = MagicMock()
        del mock_incomplete_config.data_generation.number_of_samples  # Remove required field
        mock_read_config.return_value = mock_incomplete_config

        config_manager = ConfigurationManager()
        with self.assertRaises(AttributeError):
            config_manager.get_data_generation_config()


if __name__ == "__main__":
    unittest.main()
