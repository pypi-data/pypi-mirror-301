import warnings, os, json
from collections import ChainMap
from typing import Callable, overload, final
from pathlib import Path
from pandas.errors import MergeError
import pandas as pd
from jinja2 import Template

from mipi_datamanager import query, odbc, generate_inserts
from mipi_datamanager.core import common as com
from mipi_datamanager.core import meta
from mipi_datamanager.types import JoinLiterals, Mask
from mipi_datamanager.errors import ConfigError
from mipi_datamanager.core.jinja import JinjaWorkSpace, JinjaRepo


def _get_df_and_sql_from_jinja_template(jenv, script_path, connection, jinja_parameters_dict): # TODO these are redundant
    df = jenv.execute_file(script_path, connection, jinja_parameters_dict)
    sql = jenv.resolve_file(script_path, jinja_parameters_dict)
    del jenv
    return df, sql


def _get_df_and_sql_from_jinja_repo(jinja_repo_source, inner_path, connection, jinja_parameters_dict):
    jenv = JinjaRepo(jinja_repo_source.root_dir)
    return _get_df_and_sql_from_jinja_template(jenv, inner_path, connection, jinja_parameters_dict)


def _get_df_and_sql_from_jinja(script_path, connection, jinja_parameters_dict):
    path = Path(script_path)
    jenv = JinjaWorkSpace(path.parent)
    return _get_df_and_sql_from_jinja_template(jenv, path.name, connection, jinja_parameters_dict)


def _get_df_and_sql_from_sql(script_path, format_parameters_list, connection):
    df = query.execute_sql_file(script_path, connection, format_parameters_list)
    sql = query.read_sql(script_path, format_parameters_list)
    return df, sql


def _maybe_get_frame_name(frame_name, script_path):
    return frame_name or Path(script_path).stem


def _get_config_from_master(inner_path, jinja_repo_source):
    _inner_path = Path(inner_path)
    with open(os.path.join(jinja_repo_source.root_dir, "master_config.json"), 'r') as f:
        master_config = json.load(f)
    return master_config[str(_inner_path.parent).replace("\\", "/")][str(_inner_path.name)]


class _FormattedFunctions:
    def __init__(self, format_func_dict: dict | ChainMap = None):

        self._validate(format_func_dict)
        _format_func_dict = format_func_dict or dict()
        self.format_func_dict = _format_func_dict

    def _validate(self, format_func_dict):
        '''assert that the single func is callable and the dict is a dict of callables'''

        if format_func_dict:
            for k, v in format_func_dict.items():
                if not callable(v):
                    raise ValueError(f"Function {k} must be callable")

    @final
    def format_series(self, series):

        if not isinstance(series, pd.Series):
            raise ValueError(f"series must be pd.Series, got {type(series)}")

        key = series.name
        if key in self.format_func_dict:
            format_func = self.format_func_dict[key]
            return format_func(series)
        else:
            return series


class _FormattedJoinOperation:
    def __init__(self, format_funcs: list[_FormattedFunctions]):
        self._validate(format_funcs)
        format_dicts = [i.format_func_dict for i in format_funcs]
        self._final_dict = ChainMap(*format_dicts)
        self.final_formatter = _FormattedFunctions(self._final_dict)

    def _validate(self, format_funcs):
        if not isinstance(format_funcs, list):
            raise ValueError(f"format_funcs must be a list, got {type(format_funcs)}")
        else:
            for f in format_funcs:
                if not isinstance(f, _FormattedFunctions):
                    raise ValueError(f"formatter must be type of _FormattedFunctions, got {type(f)}")

    @overload
    def _format_df_slice(self, slice: pd.DataFrame) -> pd.DataFrame:
        ...

    @overload
    def _format_df_slice(self, slice: pd.Series) -> pd.Series:
        ...

    def _format_df_slice(self, df):
        if isinstance(df, pd.DataFrame):
            for c in df.columns:
                df[c] = self.final_formatter.format_series(df[c])
        elif isinstance(df, pd.Series):
            df = self.final_formatter.format_series(df)

        return df

    def _format_slice_by_key(self, df, key):
        key = com._maybe_convert_tuple_to_list(key)
        df[key] = self._format_df_slice(df[key])
        return df

    def _format_pair_by_keys(self, df, key, use_index):
        if not use_index:
            _df = self._format_slice_by_key(df, key)
        else:
            _df = df
        return _df

    # def _format_index(self,df): # TODO
    #     df.index = #self.final_formatter.format_series()

    @final
    def format_incoming_df(self, df):  # , on=None, side_on=None, use_index=False):
        for c in df.columns:
            if c in self._final_dict:
                df[c] = self.final_formatter.format_series(df[c])
        return df

    def validate_join(self):
        pass


class DataManager:
    """
    Creates an object to pull data from databases. Automatically keeps track of the changing target population.

    Contains:
    - Base Inserts
    - Target Inserts
    - Base Population
    - Target Population
    - Frames

    Each Frame represents one query which was performed and incorporated into the target population
    - df_query: dataframe for the specific query
    - df_target: target dataframe at the time this query was used
    - dimensions: rows and columns of the dataframes
    - config: executable SQL object

    Each Config contains an executable SQL object
    - Jinja Template
    - Jinja arguments inserted into the template
    - ODBC connection


    Back end: this object is centered around storing frames. all functionality is derived from these frames

    """

    def __init__(self, frame: meta.Frame,
                 jinja_repo_source: JinjaRepo = None, #TODO maybe change name to jinja_repo
                 store_deep_frames=False,
                 store_deep_base=False,
                 default_format_func_dict: dict = None,
                 dialect="mssql"):

        self.dialect = dialect
        self.colums_with_format_applied = []
        self.default_formatter = _FormattedFunctions(default_format_func_dict)

        if default_format_func_dict is None:
            default_format_func_dict = dict()

        self._user_added_func_dict = default_format_func_dict.copy()
        self.default_format_func_dict = default_format_func_dict.copy()
        self.jinja_repo_source = jinja_repo_source

        assert isinstance(frame, meta.Frame)
        self.frames = com.IndexedDict()

        self.store_deep_frames = store_deep_frames
        self.store_deep_base = store_deep_base

        # copy to target population, mutable, formatting done in meta.frame
        self.target_population = frame.df_query.copy()
        self.default_formatter_chain = _FormattedJoinOperation([self.default_formatter])
        self.target_population = self.default_formatter_chain.format_incoming_df(self.target_population)
        frame.set_target(self.target_population)

        self._column_sources = dict()  # stores frame_index of columns. used to add frame number as join suffix for duped cols
        self._set_column_source_from_frame(frame, 0)

        if not self.store_deep_base:
            del frame.df_query
            del frame.df_target
        self._store_frame(frame, 0)

    @classmethod
    def from_jinja_repo(cls, inner_path,
                    jinja_repo_source: JinjaRepo,
                    jinja_parameters_dict: dict = None,
                    store_deep_base=False,
                    store_deep_frames=False,
                    default_format_func_dict: dict = None,
                    dialect="mssql"):

        config = _get_config_from_master(inner_path, jinja_repo_source)

        if not config["meta"]["population"]:
            raise ConfigError(f'expected population status is True script got: {config["meta"]['population']}')

        con = jinja_repo_source.conn_list[config['meta']['connection']]
        df, sql = _get_df_and_sql_from_jinja_repo(jinja_repo_source, inner_path, con, jinja_parameters_dict)
        frame = meta.Frame(config["meta"]["name"], "JinjaRepo", df, sql=sql)

        return cls(frame,
                   jinja_repo_source=jinja_repo_source,
                   store_deep_frames=store_deep_frames,
                   store_deep_base=store_deep_base,
                   default_format_func_dict=default_format_func_dict,
                   dialect=dialect)

    def set_jinja_repo_source(self, jinja_repo_source):
        if self.jinja_repo_source:
            raise AttributeError(
                f"Mipi object {repr(self)} has already been set. Create a new mipi object, or clone this one to set a different sql repo source")
        else:
            self.jinja_repo_source = jinja_repo_source

    @classmethod
    def from_dataframe(cls, df: pd.DataFrame, frame_name=None,
                       jinja_repo_source: JinjaRepo = None,
                       store_deep_frames=False, store_deep_base=False,
                       default_format_func_dict: dict = None,
                       dialect="mssql"
                       ):
        """Create manager base population from a dataframe"""
        _frame_name = frame_name or "unnamed-dataframe"

        frame = meta.Frame(_frame_name, "Data Frame", df, None, None)
        return cls(frame, jinja_repo_source=jinja_repo_source,
                   store_deep_frames=store_deep_frames, store_deep_base=store_deep_base,
                   default_format_func_dict=default_format_func_dict,
                   dialect=dialect)

    @classmethod
    def from_sql(cls, script_path: str, connection: odbc.Odbc, format_parameters_list: list = None, frame_name=None,
                 jinja_repo_source: JinjaRepo = None,
                 store_deep_frames=False, store_deep_base=False,
                 default_format_func_dict: dict = None,
                 dialect="mssql"):
        """Create manager base population from a SQL file"""

        _frame_name = _maybe_get_frame_name(frame_name, script_path)
        df, sql = _get_df_and_sql_from_sql(script_path, format_parameters_list, connection)

        built_from = "Format SQL" if format_parameters_list else "SQL"

        frame = meta.Frame(_frame_name, built_from, df, sql=sql)
        return cls(frame, jinja_repo_source=jinja_repo_source, store_deep_frames=store_deep_frames,
                   store_deep_base=store_deep_base,
                   default_format_func_dict=default_format_func_dict, dialect=dialect)

    @classmethod
    def from_jinja(cls, script_path, connection: odbc.Odbc,
                   jinja_parameters_dict: dict = None,
                   frame_name: str = None,
                   jinja_repo_source: JinjaRepo = None,
                   store_deep_frames=False, store_deep_base=False,
                   default_format_func_dict: dict = None,
                   dialect="mssql"):

        _frame_name = _maybe_get_frame_name(frame_name, script_path)

        df, sql = _get_df_and_sql_from_jinja(script_path, connection, jinja_parameters_dict)

        frame = meta.Frame(_frame_name, "Jinja", df, sql=sql)

        return cls(frame, jinja_repo_source=jinja_repo_source, store_deep_frames=store_deep_frames,
                   store_deep_base=store_deep_base,
                   default_format_func_dict=default_format_func_dict, dialect=dialect)

    @classmethod
    def from_excel(cls, excel_path: str, frame_name: str = None,
                   jinja_repo_source: JinjaRepo = None,
                   store_deep_frames=False, store_deep_base=False,
                   default_format_func_dict: dict = None,
                   excel_sheet_name: str | int | None = None,
                   dialect="mssql"):
        """Create manager base population from an excel file"""
        _frame_name = _maybe_get_frame_name(frame_name, excel_path)
        df = pd.read_excel(excel_path, sheet_name=excel_sheet_name or 0)
        frame = meta.Frame(_frame_name, "Excel", df)
        return cls(frame, jinja_repo_source=jinja_repo_source, store_deep_frames=store_deep_frames,
                   store_deep_base=store_deep_base,
                   default_format_func_dict=default_format_func_dict,
                   dialect=dialect)

    def _store_frame(self, frame: meta.Frame, idx) -> None:
        """ to store a frame including its index"""
        alias = f"{frame.name}_{idx}"
        self.frames[alias] = frame

    ##############################################################################################
    # Target Data Joins
    ##############################################################################################

    def join_from_jinja_repo(self, inner_path, how: JoinLiterals = "left", jinja_parameters_dict: dict = None,
                         format_func_dict=None, left_on = None, left_index = None):

        if jinja_parameters_dict is None:
            _jinja_parameters_dict = {}
        else:
            _jinja_parameters_dict = jinja_parameters_dict

        config = _get_config_from_master(inner_path, self.jinja_repo_source) #TODO replace with JinjaRepo.pull

        if config["meta"]["population"]:
            raise ConfigError(f'expected population status is False script got: {config["meta"]['population']}')

        right_on = config["meta"]["join_key"]


        if left_on:
            if isinstance(left_on, str):
                rename_dict = {left_on: right_on}
            else:
                rename_dict = {k: v for k, v in zip(left_on, right_on)}
        else:
            rename_dict = None

        con = self.jinja_repo_source.conn_list[config['meta']['connection']]

        sql = self.resolve_join_jinja_repo_template(inner_path, right_on,jinja_parameters_dict,rename_columns=rename_dict, table_name= config["meta"]["insert_table_name"])
        df = query.execute_sql(sql,con)

        frame = meta.Frame(config["meta"]["name"], "JinjaRepo", df, sql=sql)

        self._join_from_frame(frame, right_on, how, format_func_dict, None, None, False,
                              False)  # TODO add join funcs to configs

    def join_from_dataframe(self, df: pd.DataFrame, on=None, how: JoinLiterals = "left", frame_name: str = None,
                            format_func_dict=None,
                            left_on=None, right_on=None,
                            left_index=False, right_index=False):
        """Joins a dataframe into the target population"""

        _frame_name = frame_name or "unnamed-dataframe"
        frame = meta.Frame(_frame_name, "Data Frame", df.copy(), None, None)
        self._join_from_frame(frame, on, how, format_func_dict, left_on, right_on, left_index,
                              right_index)

    def join_from_excel(self, excel_path: str, on: str = None, how: JoinLiterals = "left", frame_name: str = None,
                        excel_sheet_name=None, format_func_dict=None,
                        left_on=None, right_on=None,
                        left_index=False, right_index=False):
        """Joins the a dataframe into the target population"""
        _frame_name = _maybe_get_frame_name(frame_name, excel_path)
        df = pd.read_excel(excel_path, sheet_name=excel_sheet_name or 0)
        frame = meta.Frame(_frame_name, "Excel", df, None, None)
        self._join_from_frame(frame, on, how, format_func_dict, left_on, right_on, left_index,
                              right_index)

    def join_from_format_sql(self, script_path: str, connection, on=None, how: JoinLiterals = "left",
                             format_parameters_list: list = None,
                             frame_name: str = None, format_func_dict=None,
                             left_on=None, right_on=None,
                             left_index=False, right_index=False):
        """Joins the results of a sql file into the target population.
        assumes there script has a {} placeholder for insert statements.
        On parameter gets used as inserts."""

        _frame_name = _maybe_get_frame_name(frame_name, script_path)

        if on:
            _on = on
            rename_dict = None
        elif left_on: #TODO add index
            _on = right_on
            if isinstance(left_on, str):
                rename_dict = {left_on: right_on}
            else:
                rename_dict = {k: v for k, v in zip(left_on, right_on)}
        # elif left_index: #TODO add index
        #     _on =
        #     if isinstance(left_on, str):
        #         rename_dict = {left_on: right_on}
        #     else:
        #         rename_dict = {k: v for k, v in zip(left_on, right_on)}
        else:
            raise MergeError("Must define either 'on' or 'left/right")


        sql = self.resolve_join_format_sql_file(script_path,_on,format_parameters_list,rename_columns=rename_dict)
        df = query.execute_sql(sql,connection)

        frame = meta.Frame(_frame_name, "Format SQL", df, sql=sql)
        self._join_from_frame(frame, on, how, format_func_dict, left_on, right_on, left_index,
                              right_index)

    def join_from_jinja(self, script_path, connection: odbc.Odbc, on=None, how: JoinLiterals = "left",
                        jinja_parameters_dict=None,
                        frame_name=None, format_func_dict=None,
                        left_on=None, right_on=None,
                        left_index=False, right_index=False,
                        insert_table_name = "MiPiTempTable"):

        _frame_name = _maybe_get_frame_name(frame_name, script_path)

        if on:
            _on = on
            rename_dict = None
        elif left_on:
            _on = right_on
            if isinstance(left_on, str):
                rename_dict = {left_on: right_on}
            else:
                rename_dict = {k: v for k, v in zip(left_on, right_on)}
        else:
            raise MergeError("Must define either 'on' or 'left/right")

        # elif left_index: # TODO
        #     pass

        sql = self.resolve_join_jinja_template(script_path,_on, jinja_parameters_dict=jinja_parameters_dict, rename_columns=rename_dict, insert_table_name=insert_table_name)
        df = query.execute_sql(sql, connection)

        frame = meta.Frame(_frame_name, "Jinja", df, sql=sql)
        self._join_from_frame(frame, on, how, format_func_dict, left_on, right_on, left_index,
                              right_index)

    def _join_from_frame(self, frame: meta.Frame, on: str, how: JoinLiterals,
                         format_func_dict, left_on, right_on, left_index, right_index):
        """Joins a frame into target population. used by used join functions"""

        local_join_formatter = _FormattedFunctions(format_func_dict)
        final_formatter = _FormattedJoinOperation([local_join_formatter, self.default_formatter])
        frame.df_query = final_formatter.format_incoming_df(frame.df_query)

        self.target_population = self.target_population.merge(frame.df_query, how=how, on=on, left_on=left_on,
                                                              right_on=right_on, left_index=left_index,
                                                              right_index=right_index)
        frame_idx = len(self.frames)
        frame.set_target(self.target_population)
        self._set_column_source_from_frame(frame, frame_idx)

        if not self.store_deep_frames:
            del frame.df_query
            del frame.df_target

        self._store_frame(frame, frame_idx)

    def _set_column_source_from_frame(self, frame, idx) -> None:
        """
        appends the source column dictionary
        self.source_columns[column_name] = frame_index
        also renames duplicated columns x,y -> '~frame'
        rename also changes the source column dictionary, however it keeps the original value which contains no suffix\
        this identifies any future use of that column as a dupe.
        """

        # loop current frames query
        for column in frame.query_columns:

            # add new column to source dict
            if column not in self._column_sources:
                # no dupe -> assign to source columnm
                self._column_sources[column] = idx

            # for duplicate columns: add to source list and rename suffixes
            if ((f"{column}_x" in self.target_population.columns)
                    and (f"{column}_y" in self.target_population.columns)):
                warnings.warn(
                    f"\nColumn {column} was duplicated during a join.\nThe duplicated column suffixes were renamed in accordance with their origin frame.\ncoalesce duplicate columns with mipi.",
                    stacklevel=2)

                # col origonal source
                old_idx = self._column_sources[column]

                # assign rename vals for join suffixes x,y -> '~frame'
                x_old_target_column_name = f"{column}_x"
                y_old_target_column_name = f"{column}_y"
                x_new_target_column_name = f"{column}~{self.frames[old_idx].name}_{old_idx}"
                y_new_target_column_name = f"{column}~{frame.name}_{idx}"

                # rename target
                self.target_population = self.target_population.rename(
                    columns={x_old_target_column_name: x_new_target_column_name,
                             y_old_target_column_name: y_new_target_column_name})

                # rename source dict to deal with future dupes
                self._column_sources[x_new_target_column_name] = old_idx
                self._column_sources[y_new_target_column_name] = idx

            # third+ dupe will already exist in column key and will be added to the target without a suffix, needs rename
            if (column in self._column_sources
                    and any(f"{column}~{frame.name}" in col for col in self._column_sources)
                    and column in self.target_population.columns):
                self._column_sources[f"{column}~{frame.name}_{idx}"] = idx
                self.target_population = self.target_population.rename(columns={column: f"{column}~{frame.name}_{idx}"})

    ##############################################################################################
    # Target Data Transformations
    ##############################################################################################

    def filter(self, mask: Mask):
        """Filters the target population using a mask.
        use self.trgt[] for the mask"""
        self.target_population = self.target_population[mask]

    def clone(self, base_name=None,
              change_jinja_repo_source=None,
              store_deep_frames=False, store_deep_base=False,
              rename_columns_dict=None,
              add_to_default_format_func_dict=None):

        df = self.trgt.copy()

        _jinja_repo_source = change_jinja_repo_source or self.jinja_repo_source

        # rename columns to declare new PKs
        if rename_columns_dict is not None:
            df = df.rename(columns=rename_columns_dict)

        base_name = base_name or f"Clone from: {repr(self)}"

        assert isinstance(add_to_default_format_func_dict, (dict, type(None))), "Format Dict must be type dict"
        if add_to_default_format_func_dict is not None:
            if self._user_added_func_dict is not None:
                new_format_dict = self._user_added_func_dict
            else:
                new_format_dict = dict()
            for k, v in add_to_default_format_func_dict.items():
                new_format_dict.update({k: v})
        else:
            new_format_dict = self._user_added_func_dict

        frame = meta.Frame(base_name, "Clone", df, None, None)

        cls = self.__class__

        mipi2 = cls(frame, jinja_repo_source=_jinja_repo_source,
                    store_deep_frames=store_deep_frames, store_deep_base=store_deep_base,
                    default_format_func_dict=new_format_dict)

        return mipi2

    def get_insert_statements(self, key: str, frame=None, rename_columns: dict | None = None):  # TODO test from specific frame
        """Get the most current list of inserts where 'on' is the insert key"""

        df = frame.df_query if frame is not None else self.trgt
        if rename_columns:
            df = df.rename(columns=rename_columns)
        if self.dialect == 'mssql':
            if isinstance(key, str):
                return generate_inserts.generate_mssql_inserts(df[[key]], make_temptable=True)
            elif isinstance(key, (tuple, list)):
                key = com._maybe_convert_tuple_to_list(key)
                return generate_inserts.generate_mssql_inserts(df[key], make_temptable=True)

    def _drop_temp_table(self, sql, temp_tablename = "MiPiTempTable"):
        return sql + f"\nDROP TABLE #{temp_tablename};\n"

    def resolve_join_format_sql(self, sql: str, key: str, format_parameters_list=None, frame=None,
                                rename_columns: dict | None = None):
        inserts = self.get_insert_statements(key, frame=frame, rename_columns=rename_columns)
        if format_parameters_list:
            _format_parameters_list = [inserts] + format_parameters_list
        else:
            _format_parameters_list = [inserts]

        sql = sql.format(inserts)
        sql = self._drop_temp_table(sql)
        return sql

    def resolve_join_format_sql_file(self, file_path: str, key: str, format_parameters_list=None, frame=None,
                                     rename_columns: dict | None = None):
        sql = self._read_file(file_path)
        return self.resolve_join_format_sql(sql, key, format_parameters_list, frame = frame,rename_columns = rename_columns)

    def _get_sql_from_jinja_template(self, jenv, script_path, jinja_parameters_dict):
        sql = jenv.resolve_file(script_path, jinja_parameters_dict)
        del jenv
        return sql

    def _maybe_get_jinja_insert_dict(self,key,jinja_parameters_dict = None, frame = None,rename_columns= None, insert_table_name:str = "MiPiTempTable"):
        if jinja_parameters_dict:
            jinja_parameters_dict[insert_table_name] = self.get_insert_statements(key,frame = frame,rename_columns = rename_columns)
        else:
            jinja_parameters_dict = {insert_table_name: self.get_insert_statements(key,frame = frame,rename_columns = rename_columns)}
        return jinja_parameters_dict
    def resolve_join_jinja_repo_template(self, inner_path, key, jinja_parameters_dict, frame=None,
                                     rename_columns: dict | None = None, table_name:str = "MiPiTempTable" ):
        jenv = JinjaRepo(self.jinja_repo_source.root_dir)
        jinja_parameters_dict = self._maybe_get_jinja_insert_dict(key, jinja_parameters_dict,frame,rename_columns, insert_table_name = table_name)
        sql = self._get_sql_from_jinja_template(jenv, inner_path, jinja_parameters_dict)
        sql = self._drop_temp_table(sql)
        return sql

    def resolve_join_jinja_template(self, script_path, key, jinja_parameters_dict, frame=None,
                                    rename_columns: dict | None = None, insert_table_name:str = "MiPiTempTable"):
        path = Path(script_path)
        jenv = JinjaWorkSpace(path.parent)
        jinja_parameters_dict = self._maybe_get_jinja_insert_dict(key, jinja_parameters_dict,frame,rename_columns, insert_table_name = insert_table_name)
        sql = self._get_sql_from_jinja_template(jenv, path.name, jinja_parameters_dict)
        sql = self._drop_temp_table(sql)
        return sql

    def resolve_join_jinja(self, script:str, key:str, jinja_parameters_dict:dict, frame=None,
                                    rename_columns: dict | None = None, insert_table_name:str = "MiPiTempTable"):
        template = Template(script)
        jinja_parameters_dict = self._maybe_get_jinja_insert_dict(key, jinja_parameters_dict, frame, rename_columns,
                                                                  insert_table_name=insert_table_name)
        sql = template.render(jinja_parameters_dict)
        return self._drop_temp_table(sql)
    def _read_file(self, path):
        with open(path, "r") as f:
            contents = f.read()
        return contents

    @property
    def base_population(self):
        if self.store_deep_base:
            return self.frames[0].df_query  # first frame
        else:
            return "base population not available because store_deep_frames is False"

    @property
    def trgt(self):
        return self.target_population

    def print_target_columns(self):
        print(self.target_population.columns.tolist())

    @property
    def duplicated_columns(self):
        return [col for col in self.target_population.columns if "~" in col]  # TODO check if it is a frame name
