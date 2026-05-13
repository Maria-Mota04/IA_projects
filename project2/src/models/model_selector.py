import pandas as pd


class ModelSelector:
    def __init__(self, metric: str = "F1"):
        self.metric = metric

    def select_best(self, results_df):
        if results_df.empty or self.metric not in results_df.columns:
            return None

        df = results_df.dropna(subset=[self.metric, "Model"])
        if df.empty:
            return None

        return df.sort_values(by=self.metric, ascending=False).iloc[0]["Model"]
