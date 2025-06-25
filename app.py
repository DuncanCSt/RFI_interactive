import streamlit as st
import sqlite3
import pandas as pd

@st.cache_data
def load_data():
    conn = sqlite3.connect("rfi.db")
    df = pd.read_sql_query("SELECT * FROM rfi_table", conn)
    conn.close()
    return df

st.title("My Streamlit App")
df = load_data()
st.write(df.head())