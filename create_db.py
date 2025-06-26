import zipfile
import sqlite3
import pandas as pd
import streamlit as st

def create_database():
    # Extract and read the zipped CSV
    with zipfile.ZipFile("mini_rfi_slice.csv.zip") as z:
        with z.open("mini_rfi_slice.csv") as f:
            rfi = pd.read_csv(f, index_col=0)

    with zipfile.ZipFile("transitions_parsed.csv.zip") as z:
        with z.open("transitions_parsed.csv") as f:
            transitions = pd.read_csv(f)

    # Create the SQLite database and write the DataFrame
    conn = sqlite3.connect("rfi.db")
    rfi.to_sql("rfi_table", conn, if_exists="replace", index=True, index_label="frequency")
    transitions.to_sql("transitions_table", conn, if_exists="replace", index=False)
    conn.close()

if __name__ == "__main__":
    create_database()