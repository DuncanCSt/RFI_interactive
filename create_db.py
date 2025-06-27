import zipfile
import sqlite3
import pandas as pd
import streamlit as st
import os

def create_database():
    # Skip database creation if both tables already exist
    db_exists = os.path.exists("rfi.db")
    if db_exists:
        return

    # Extract and read the zipped CSV
    with zipfile.ZipFile("data_slice.zip") as z:
        with z.open("data_slice.csv") as f:
            rfi = pd.read_csv(f, index_col=0)

    with zipfile.ZipFile("transitions_parsed.csv.zip") as z:
        with z.open("transitions_parsed.csv") as f:
            transitions = pd.read_csv(f)

    # Ensure the transitions table has a ``score`` column so that the app
    # can store user provided scores.  When the database is created the
    # column is initialised with empty strings.
    transitions["score"] = ""

    # Create the SQLite database and write the DataFrame
    conn = sqlite3.connect("rfi.db")
    rfi.to_sql("rfi_table", conn, if_exists="replace", index=False)
    transitions.to_sql("transitions_table", conn, if_exists="replace", index=False)
    conn.close()

if __name__ == "__main__":
    create_database()