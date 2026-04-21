import pandas as pd


class DataTransformer:

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def get_df(self):
        return self.df
    