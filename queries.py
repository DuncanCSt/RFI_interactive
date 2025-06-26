import sqlite3
import pandas as pd
import streamlit as st

## RFI Table
@st.cache_data
def load_data():
    conn = sqlite3.connect("rfi.db")
    df = pd.read_sql_query("SELECT * FROM rfi_table", conn)
    conn.close()
    return df

## Summary Table
@st.cache_data
def load_summary_data():
    conn = sqlite3.connect("rfi.db")
    df = pd.read_sql_query("SELECT * FROM summary_table", conn)
    conn.close()
    return df

## Transitions Table
@st.cache_data
def load_transitions_data():
    conn = sqlite3.connect("rfi.db")
    df = pd.read_sql_query("SELECT * FROM transitions_table", conn)
    conn.close()
    return df
