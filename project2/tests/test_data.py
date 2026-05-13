import pytest
import pandas as pd
from unittest.mock import patch, MagicMock, mock_open
from pathlib import Path
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.data.dataset_loader import DatasetLoader


class TestDatasetLoaderInit:
    """Test DatasetLoader initialization"""

    @patch("pathlib.Path.exists")
    def test_init_with_valid_file(self, mock_exists):
        """Test initialization with valid file"""
        mock_exists.return_value = True
        loader = DatasetLoader("data/valid_file.xlsx")
        assert loader.file_path == Path("data/valid_file.xlsx")

    @patch("pathlib.Path.exists")
    def test_init_with_invalid_file(self, mock_exists):
        """Test initialization with non-existent file raises FileNotFoundError"""
        mock_exists.return_value = False
        with pytest.raises(FileNotFoundError):
            DatasetLoader("data/nonexistent_file.xlsx")


class TestDatasetLoaderLoadSingleSheet:
    """Test load_single_sheet method"""

    @patch("src.data.dataset_loader.pd.read_excel")
    @patch("pathlib.Path.exists")
    def test_load_single_sheet_with_name(self, mock_exists, mock_read_excel):
        """Test loading a sheet by name"""
        mock_exists.return_value = True
        mock_df = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
        mock_read_excel.return_value = mock_df

        loader = DatasetLoader("data/test.xlsx")
        result = loader.load_single_sheet("Sheet1")

        mock_read_excel.assert_called_once()
        assert mock_read_excel.call_args[1]["sheet_name"] == "Sheet1"
        assert isinstance(result, pd.DataFrame)

    @patch("src.data.dataset_loader.pd.read_excel")
    @patch("pathlib.Path.exists")
    def test_load_single_sheet_without_name(self, mock_exists, mock_read_excel):
        """Test loading first sheet when sheet_name is None"""
        mock_exists.return_value = True
        mock_df = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
        mock_read_excel.return_value = mock_df

        loader = DatasetLoader("data/test.xlsx")
        result = loader.load_single_sheet()

        mock_read_excel.assert_called_once()
        assert isinstance(result, pd.DataFrame)


class TestDatasetLoaderLoadAllSheets:
    """Test load_all_sheets method"""

    @patch("src.data.dataset_loader.pd.ExcelFile")
    @patch("src.data.dataset_loader.pd.read_excel")
    @patch("pathlib.Path.exists")
    def test_load_all_sheets_with_source_column(
        self, mock_exists, mock_read_excel, mock_excel_file
    ):
        """Test loading all sheets with source_sheet column"""
        mock_exists.return_value = True

        # Mock ExcelFile
        mock_excel_instance = MagicMock()
        mock_excel_instance.sheet_names = ["Sheet1", "Sheet2"]
        mock_excel_file.return_value = mock_excel_instance

        # Mock read_excel to return different dataframes
        df1 = pd.DataFrame({"col1": [1, 2]})
        df2 = pd.DataFrame({"col1": [3, 4]})
        mock_read_excel.side_effect = [df1, df2]

        loader = DatasetLoader("data/test.xlsx")
        result = loader.load_all_sheets(add_source_column=True)

        assert "source_sheet" in result.columns
        assert list(result["source_sheet"].unique()) == ["Sheet1", "Sheet2"]
        assert len(result) == 4

    @patch("src.data.dataset_loader.pd.ExcelFile")
    @patch("src.data.dataset_loader.pd.read_excel")
    @patch("pathlib.Path.exists")
    def test_load_all_sheets_without_source_column(
        self, mock_exists, mock_read_excel, mock_excel_file
    ):
        """Test loading all sheets without source_sheet column"""
        mock_exists.return_value = True

        # Mock ExcelFile
        mock_excel_instance = MagicMock()
        mock_excel_instance.sheet_names = ["Sheet1", "Sheet2"]
        mock_excel_file.return_value = mock_excel_instance

        # Mock read_excel
        df1 = pd.DataFrame({"col1": [1, 2]})
        df2 = pd.DataFrame({"col1": [3, 4]})
        mock_read_excel.side_effect = [df1, df2]

        loader = DatasetLoader("data/test.xlsx")
        result = loader.load_all_sheets(add_source_column=False)

        assert "source_sheet" not in result.columns
        assert len(result) == 4


class TestDatasetLoaderListSheets:
    """Test list_sheets method"""

    @patch("src.data.dataset_loader.pd.ExcelFile")
    @patch("pathlib.Path.exists")
    def test_list_sheets(self, mock_exists, mock_excel_file):
        """Test listing all sheet names"""
        mock_exists.return_value = True

        # Mock ExcelFile
        mock_excel_instance = MagicMock()
        mock_excel_instance.sheet_names = ["Sheet1", "Sheet2", "Sheet3"]
        mock_excel_file.return_value = mock_excel_instance

        loader = DatasetLoader("data/test.xlsx")
        result = loader.list_sheets()

        assert result == ["Sheet1", "Sheet2", "Sheet3"]
        assert len(result) == 3


class TestDatasetLoaderPreview:
    """Test preview method"""

    @patch("src.data.dataset_loader.pd.read_excel")
    @patch("pathlib.Path.exists")
    def test_preview(self, mock_exists, mock_read_excel):
        """Test preview of dataset"""
        mock_exists.return_value = True

        # Mock read_excel
        mock_df = pd.DataFrame(
            {"col1": [1, 2, 3, 4, 5, 6], "col2": [10, 20, 30, 40, 50, 60]}
        )
        mock_read_excel.return_value = mock_df

        loader = DatasetLoader("data/test.xlsx")
        result = loader.preview(n=3)

        assert len(result) == 3
        assert list(result.columns) == ["col1", "col2"]
        assert result.iloc[0]["col1"] == 1
