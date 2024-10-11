import pandas as pd
from pandas import DataFrame as DataFramePandas


class EasyPandaHelpers:
    @staticmethod
    def order_pd_types_to_pd_df(pd_df: DataFramePandas, pd_types: dict) -> dict:
        if pd_df.empty:
            return pd_types

        pd_types = {key: pd_types[key] for key in pd_df.columns}
        return pd_types

    @staticmethod
    def combine_pd_types(pd_types: dict, pd_types_to_add: dict) -> dict:
        for key, value in pd_types_to_add.items():
            if key not in pd_types:
                pd_types[key] = value
        return pd_types
