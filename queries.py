import sqlite3
import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    conn = sqlite3.connect("rfi.db")
    df = pd.read_sql_query("SELECT * FROM rfi_table", conn)
    conn.close()
    return df