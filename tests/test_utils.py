import unittest
from pathlib import Path
from unittest.mock import mock_open, patch

from box import ConfigBox

from arcdemo.utils.common import read_config


class TestReadConfig(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open, read_data="key: value\n")
    @patch("yaml.safe_load", return_value={"key": "value"})
    @patch("arcdemo.logger")
    def test_read_config_success(self, mock_logger, mock_yaml, mock_file):
        """Test if config file loads correctly."""
        config_path = Path("config.yaml")
        config = read_config(config_path)

        # Assertions
        mock_file.assert_called_once_with(config_path, "r", encoding="utf-8")
        mock_yaml.assert_called_once()

        self.assertIsInstance(config, ConfigBox)
        self.assertEqual(config.key, "value")  # Check if key-value exists

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_read_config_file_not_found(self, mock_file):
        """Test if function raises FileNotFoundError when config file is missing."""
        config_path = Path("missing_config.yaml")

        with self.assertRaises(FileNotFoundError) as context:
            read_config(config_path)
        self.assertEqual(str(context.exception), f"Config file not found: {config_path}")


if __name__ == "__main__":
    unittest.main()
