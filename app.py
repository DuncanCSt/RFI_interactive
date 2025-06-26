import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from create_db import create_database  # Import the database-creation function
from create_summary_table import create_summary_table
from queries import save_transitions_data
from st_aggrid import (
    AgGrid,
    GridOptionsBuilder,
    GridUpdateMode,
    DataReturnMode,
    JsCode,
)

create_database()
create_summary_table()

st.title("My Streamlit App")

conn = sqlite3.connect("rfi.db")
summary_df = pd.read_sql_query("SELECT * FROM summary_table", conn)
transitions_df = pd.read_sql_query("SELECT * FROM transitions_table", conn)
conn.close()

# Older versions of the database might not contain the ``score`` column.
# Ensure it exists so user selections can be persisted.
if "score" not in transitions_df.columns:
    transitions_df["score"] = ""

transition_types = transitions_df["Species"].dropna().unique()
selected_value = st.sidebar.selectbox("Select Transition Type", transition_types)
filtered_transitions_df = transitions_df[transitions_df["Species"] == selected_value].copy()

# Your JS styling logic wrapped in JsCode:
row_style = JsCode("""
function(params) {
  if (params.data.score === 'fully clean') {
    return { background: 'lightgreen' };
  } else if (params.data.score === 'partially clean') {
    return { background: 'lightyellow' };
  } else if (params.data.score === 'not clean') {
    return { background: 'lightcoral' };
  }
  return {};
}
""")

gb = GridOptionsBuilder.from_dataframe(filtered_transitions_df)
gb.configure_column(
    "score",
    editable=True,
    cellEditor="agSelectCellEditor",
    cellEditorParams={"values": ["fully clean", "partially clean", "not clean"]},
)
# pass the JsCode object, not a raw string
gb.configure_grid_options(getRowStyle=row_style)
grid_options = gb.build()

grid_response = AgGrid(
    filtered_transitions_df,
    gridOptions=grid_options,
    update_mode=GridUpdateMode.VALUE_CHANGED,
    data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
    allow_unsafe_jscode=True,
)
filtered_transitions_df = grid_response["data"]

# Update ``transitions_df`` with the edited ``score`` values and persist
# the changes back to the SQLite database.
mask = transitions_df["Species"] == selected_value
transitions_df.loc[mask, "score"] = filtered_transitions_df["score"].values
save_transitions_data(transitions_df)

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
