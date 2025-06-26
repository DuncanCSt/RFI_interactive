"""Utility functions for loading data from the SQLite database used by the
interactive app."""

from __future__ import annotations

import sqlite3
from typing import Final

import pandas as pd
import streamlit as st


DEFAULT_DB_PATH: Final[str] = "rfi.db"


@st.cache_data
def load_table(table_name: str, db_path: str = DEFAULT_DB_PATH) -> pd.DataFrame:
    """Return ``table_name`` from ``db_path`` as a :class:`pandas.DataFrame`.

    Parameters
    ----------
    table_name:
        Name of the table to read from the SQLite database.
    db_path:
        Path to the SQLite database file.  Defaults to ``"rfi.db"``.

    Returns
    -------
    pandas.DataFrame
        The contents of ``table_name``.
    """

    with sqlite3.connect(db_path) as conn:
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    return df


def load_data(db_path: str = DEFAULT_DB_PATH) -> pd.DataFrame:
    """Load the ``rfi_table`` from the database."""

    return load_table("rfi_table", db_path=db_path)


def load_summary_data(db_path: str = DEFAULT_DB_PATH) -> pd.DataFrame:
    """Load the ``summary_table`` from the database."""

    return load_table("summary_table", db_path=db_path)


def load_transitions_data(db_path: str = DEFAULT_DB_PATH) -> pd.DataFrame:
    """Load the ``transitions_table`` from the database."""

    return load_table("transitions_table", db_path=db_path)


def save_transitions_data(df: pd.DataFrame, db_path: str = DEFAULT_DB_PATH) -> None:
    """Persist ``df`` to the ``transitions_table`` of ``db_path``."""

    with sqlite3.connect(db_path) as conn:
        df.to_sql("transitions_table", conn, if_exists="replace", index=False)

