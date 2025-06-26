import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from create_db import create_database  # Import the database-creation function
from create_summary_table import create_summary_table  

create_database()
create_summary_table()

st.title("My Streamlit App")

conn = sqlite3.connect("rfi.db")
summary_df = pd.read_sql_query("SELECT * FROM summary_table", conn)
transitions_df = pd.read_sql_query("SELECT * FROM transitions_table", conn)
conn.close()

st.write(transitions_df.head())

transition_types = transitions_df["Species"].dropna().unique()
selected_value = st.sidebar.selectbox("Select Transition Type", transition_types)
filtered_transitions_df = transitions_df[transitions_df["Species"] == selected_value]

fig, ax = plt.subplots()
ax.plot(summary_df['frequency'], summary_df['mean'], alpha=0.5, label='Mean')
plt.fill_between(summary_df['frequency'],
                 summary_df['mean'] - summary_df['std'],
                 summary_df['mean'] + summary_df['std'],
                 alpha=0.2, label='1 std')

ax.scatter(summary_df['frequency'], summary_df['trace_1'], alpha=0.5, s=1, label='Traces')
for col in ['trace_' + str(i) for i in range(2, 4)]:
    ax.scatter(summary_df['frequency'], summary_df[col], alpha=0.5, s=1)

for frequency in filtered_transitions_df['Frequency (MHz)']:
    ax.axvline(x=frequency, color='red', linestyle='--', alpha=0.5)

ax.set_xlabel("Frequency")
ax.set_ylabel("Mean (log rescaled)")
ax.set_title("Mean vs Frequency")
ax.legend()
ax.set_xlim(1000, 1600)
st.pyplot(fig)
