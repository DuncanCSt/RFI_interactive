from typing import Final
import pandas as pd
import numpy as np
import sqlite3
from helper_functions import convert_frequency_to_index, kernel_regression
import os
from queries import load_data  # Assuming load_data is defined in queries.py

MMAP_PATH: Final[str] = "/srv/data/drao-rfi/calibrated/RFInd-calibrated-2024-10-08T12.sigmf-data"
F_MIN: Final[float] = 300.0  # MHz
F_MAX: Final[float] = 1600.0  # MHz

def create_summary_table(df: pd.DataFrame = None):

    # Check if the summary table already exists in the SQLite database
    db_path = "rfi.db"
    table_exists = False
    if os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='summary_table';")
        table_exists = cursor.fetchone() is not None
        conn.close()

    if table_exists:
        return

    # Check if the MMAP_PATH exists
    if os.path.exists(MMAP_PATH):
        rfi_data = np.memmap(MMAP_PATH, dtype='f4').reshape(-1, 600000)
        t1 = 500
        t2 = 1500
        i1 = convert_frequency_to_index(F_MIN)
        i2 = convert_frequency_to_index(F_MAX)

        rfi_data = rfi_data[t1:t2, i1:i2]
        h = 90
        num_neighbors = 300
    else: # Use mini_rfi_slice.csv if MMAP_PATH does not exist
        rfi_data = load_data()
        h = 1
        num_neighbors = 10

    rfi_data = np.log(np.where(rfi_data > 1e-25, rfi_data, 1e-25))  # ignore non-positive values

    # min-max scale rfi_data from 0 to 1
    data_min = np.nanmin(rfi_data)
    data_max = np.nanmax(rfi_data)
    rfi_data = (rfi_data - data_min) / (data_max - data_min)

    # geometric mean (ignore non‐positive values)
    mean = np.nanmean(rfi_data, axis=0)

    # geometric std (multiplicative): exp(std(log(x))) ignoring non‐positive
    std  = np.nanstd(rfi_data, axis=0)

    min_cutoff = np.percentile(mean, 1)
    max_cutoff = np.percentile(mean, 90)

    X_train = np.arange(0, len(mean))
    y_train = np.clip(mean, min_cutoff, max_cutoff)
    x_predictions = X_train
    baseline = np.array([kernel_regression(X_train, y_train, X, h=h, num_neighbors=num_neighbors) for X in x_predictions])

    # create summary table
    trace_indices = np.linspace(0, rfi_data.shape[0] - 1, 5, dtype=int)
    summary_df = pd.DataFrame({
        'frequency': np.linspace(F_MIN, F_MAX, rfi_data.shape[1]),
        'baseline': baseline,
        'mean': mean,
        'std': std,
        'trace_1': rfi_data[trace_indices[0], :],
        'trace_2': rfi_data[trace_indices[1], :],
        'trace_3': rfi_data[trace_indices[2], :],
        'trace_4': rfi_data[trace_indices[3], :],
        'trace_5': rfi_data[trace_indices[4], :]
    })

    # Create the SQLite database and write the DataFrame
    conn = sqlite3.connect("rfi.db")
    summary_df.to_sql("summary_table", conn, if_exists="replace", index=False)
    conn.close()
