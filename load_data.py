import zipfile
import sqlite3
import pandas as pd

# Extract and read the zipped CSV
with zipfile.ZipFile("mini_rfi_slice.csv.zip") as z:
    with z.open("data.csv") as f:
        df = pd.read_csv(f)

# Create the SQLite database and write the DataFrame
conn = sqlite3.connect("rfi.db")
df.to_sql("rfi_table", conn, if_exists="replace", index=False)
conn.close()