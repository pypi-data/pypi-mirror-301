import warnings
from typing import Callable
import pandas as pd

class FormatDict(dict):
    """
    A dictionary child class designed to store format functions.
    """
    def update_group(self,columns:list, func:Callable) -> None:
        """
        Updates several keys of a dicitonary to all have the specified function as their value.

        :param func: callable function to set as the value
        :param columns: list of columns to set value on
        :return: None
        """
        for c in columns:
            self[c] = func


def _drop_na(series):
    if series.isna().any():
        series = series.dropna()
        warnings.warn("Na values were dropped during formatting.")
    return series


def cast(data_type):
    def cast_func(series):
        series = _drop_na(series)
        return series.astype(data_type)

    return cast_func


def cast_int_str():
    def cast_func(series):
        series = _drop_na(series)
        return series.astype("int64", errors="ignore").astype(str, errors="ignore")

    return cast_func


def cast_padded_int_str(value_length):
    def cast_func(series) -> pd.Series:
        series = _drop_na(series)
        cast_int_str_func = cast_int_str()
        series = cast_int_str_func(series)

        return series.where(~series.str.startswith('-'),
                            '-' + series.str[1:].str.rjust(value_length, "0")).str.rjust(value_length, "0")

    return cast_func


def cast_as_datetime():
    def cast_func(series: pd.Series) -> pd.Series:
        _series = _drop_na(series)
        _series = pd.to_datetime(_series)
        return series

    return cast_func


def cast_as_datetime_string(format_code):
    def cast_func(series: pd.Series):
        _series = _drop_na(series)
        _series = pd.to_datetime(_series)
        _series = _series.dt.strftime(format_code)
        return _series

    return cast_func


def cast_as_iso_date_string(date_delim="-", time_delim=":"):
    def cast_func(series: pd.Series):
        _series = _drop_na(series)
        format_string = f"%Y{date_delim}%m{date_delim}%d"
        if time_delim:
            format_string += f" %H{time_delim}%M{time_delim}%S"
        format_func = cast_as_datetime_string(format_string)
        return format_func(series)

    return cast_func


def cast_as_american_date_string(date_delim="/", time_delim=":"):
    def cast_func(series: pd.Series) -> pd.Series:
        _series = _drop_na(series)
        format_string = f"%m{date_delim}%d{date_delim}%Y"
        if time_delim:
            format_string += f" %H{time_delim}%M{time_delim}%S"
        format_func = cast_as_datetime_string(format_string)
        return format_func(series)

    return cast_func
