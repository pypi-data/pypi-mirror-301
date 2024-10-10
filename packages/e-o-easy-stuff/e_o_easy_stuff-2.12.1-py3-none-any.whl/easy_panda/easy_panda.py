import pandas as pd
from pandas import DataFrame as DataFramePandas

class EasyPanda:
    def __init__(self, pd_df: DataFramePandas):
        self._pd_df = pd_df

    @staticmethod
    def create(pd_df: DataFramePandas = None) -> 'EasyPanda':
        return EasyPanda(pd_df)

    @property
    def pd_df(self) -> DataFramePandas:
        return self._pd_df

    @pd_df.setter
    def pd_df(self, value: DataFramePandas):
        self._pd_df = value

    def from_dict(self, records: dict) -> 'EasyPanda':
        self._pd_df = pd.DataFrame.from_dict(records)
        return self

    def from_list(self, records: list[dict]) -> 'EasyPanda':
        self._pd_df = pd.DataFrame(records)

        return self

    def from_tuple(self, records: list[tuple]) -> 'EasyPanda':
        self._pd_df = pd.DataFrame(records)

        return self

    def from_json_normalize(self, records: list[dict]) -> 'EasyPanda':
        self._pd_df = pd.json_normalize(records)
        return self
