import pandas as pd
from collections import namedtuple
from mipi_datamanager.types import BuildLiterals

Dim = namedtuple("dimension", ["rows", "columns"])


class Frame:
    """
    A snapshot into the state of data object
    This class builds the output for a MiPi table
    Some variables only apply to builds from config
    """

    def __init__(self, name: str,
                 built_from: BuildLiterals,
                 df_query: pd.DataFrame,
                 df_target: pd.DataFrame | None = None,
                 sql: str | None = None,
                 store_deep: bool = True):

        self.store_deep = store_deep
        self.df_query = df_query
        self.df_target = df_target
        self.name = name
        self.built_from = built_from
        self.sql = sql

        self.query_dimension = self._get_dimension(df_query)
        self.query_columns = self._get_columns(df_query)

        if df_target:
            self.set_target(df_target)


    def set_target(self, df_target: pd.DataFrame):
        """Set target for the frame as the current state of the data objects target population"""

        if self.store_deep:
            self.df_target = df_target

        self.target_dimension = self._get_dimension(df_target)
        self.target_columns = self._get_columns(df_target)

    @staticmethod
    def _get_dimension(df: pd.DataFrame) -> Dim:
        return Dim(df.shape[0], df.shape[1])

    @staticmethod
    def _get_columns(df: pd.DataFrame) -> list:
        return list(df.columns)

