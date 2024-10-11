import pandas as pd
from pandas import DataFrame as DataFramePandas

from easy_panda.easy_panda_type import EasyPandaType


class EasyPandaHelpers:
    @staticmethod
    def order_pd_types_to_pd_df(pd_df: DataFramePandas, pd_types: dict[str, EasyPandaType]) -> dict[str, EasyPandaType]:
        if pd_df.empty:
            return pd_types

        pd_types = {key: pd_types[key] for key in pd_df.columns}
        return pd_types

    @staticmethod
    def combine_pd_types(pd_types: dict[str, EasyPandaType], pd_types_to_add: dict[str, EasyPandaType]) -> dict[
        str, EasyPandaType]:
        for key, value in pd_types_to_add.items():
            if key not in pd_types:
                pd_types[key] = value
        return pd_types
