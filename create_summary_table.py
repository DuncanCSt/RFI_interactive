import pandas as pd
import numpy as np
import sqlite3
from queries import load_data  # Assuming load_data is defined in queries.py

def create_summary_table(df: pd.DataFrame = None):

    if df is None:
        df = load_data()

    # slice out the block we want to summarize
    cols = [col for col in df.columns if col != 'frequency']
    data_slice = np.log(np.where(df[cols] > 1e-25, df[cols], np.nan))  # ignore non-positive values

    # min-max scale data_slice from 0 to 1
    data_min = np.nanmin(data_slice)
    data_max = np.nanmax(data_slice)
    data_slice = (data_slice - data_min) / (data_max - data_min)

    # geometric mean (ignore non‐positive values)
    mean = data_slice.mean(axis=1)

    # geometric std (multiplicative): exp(std(log(x))) ignoring non‐positive
    std  = np.nanstd(data_slice, axis=1)

    # create summary table
    summary_df = pd.DataFrame({
        'frequency': df['frequency'],
        'mean': mean,
        'std': std,
        'trace_1': data_slice[:, 0],
        'trace_2': data_slice[:, 1],
        'trace_3': data_slice[:, 2],
        'trace_4': data_slice[:, 3],
        'trace_5': data_slice[:, 4]
    })

    # Create the SQLite database and write the DataFrame
    conn = sqlite3.connect("rfi.db")
    summary_df.to_sql("summary_table", conn, if_exists="replace", index=False)
    conn.close()
