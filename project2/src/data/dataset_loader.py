from pathlib import Path
import pandas as pd


class DatasetLoader:
    """
    Responsible only for loading raw data from Excel files.
    """

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {self.file_path}")

    def load_single_sheet(self, sheet_name: str = None) -> pd.DataFrame:
        """
        Load a single sheet from Excel.
        If sheet_name is None, loads first sheet.
        """

        if sheet_name:
            return pd.read_excel(self.file_path, sheet_name=sheet_name)

        return pd.read_excel(self.file_path)

    def load_all_sheets(self, add_source_column: bool = False) -> pd.DataFrame:
        """
        Load all sheets and merge into one DataFrame.
        """

        excel_file = pd.ExcelFile(self.file_path)

        dfs = []

        for sheet in excel_file.sheet_names:
            df = pd.read_excel(excel_file, sheet_name=sheet)

            if add_source_column:
                df["source_sheet"] = sheet

            dfs.append(df)

        return pd.concat(dfs, ignore_index=True)

    def list_sheets(self):
        """
        Return all sheet names.
        """

        return pd.ExcelFile(self.file_path).sheet_names

    def preview(self, n: int = 5, sheet_name: str = None):
        """
        Quick preview of dataset.
        """

        df = self.load_single_sheet(sheet_name)
        return df.head(n)
