import streamlit as st

from create_db import create_database
from create_summary_table import create_summary_table
from queries import (
    load_summary_data,
    load_transitions_data,
    save_transitions_data,
)
from editable_tables import editable_transitions_table
from plots import plot_summary_with_transitions

# Ensure the SQLite database and summary table exist
create_database()
create_summary_table()

st.title("My Streamlit App")

summary_df = load_summary_data()
transitions_df = load_transitions_data()

transition_types = transitions_df["Species"].dropna().unique()
selected_value = st.selectbox(
    "Select Transition Type", transition_types
)
filtered_transitions_df = transitions_df[
    transitions_df["Species"] == selected_value
].copy()

# Download button to save the full ``transitions_df`` as a CSV file
csv = transitions_df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Download transitions table as CSV",
    data=csv,
    file_name="transitions_df.csv",
    mime="text/csv",
)

# Display editable table and get grid response (including selected rows)
grid_response = editable_transitions_table(filtered_transitions_df)
edited_df = grid_response["data"]

# Extract selected row (if any) and grab the frequency value
selected_rows = grid_response.get("selected_rows")
if selected_rows is not None and not selected_rows.empty:
    selected_frequency = selected_rows.iloc[0]["Frequency (MHz)"]
    # Define an x_range; for instance, +/- 5 around selected frequency:
    x_range = (selected_frequency - 5, selected_frequency + 5)
else:
    # Fallback, use full range or a default value
    x_range = (min(summary_df["frequency"]), max(summary_df["frequency"]))

# Update transitions_df with the edited score values and persist them
mask = transitions_df["Species"] == selected_value
transitions_df.loc[mask, "score"] = edited_df["score"].values
save_transitions_data(transitions_df)

# Plot results using the custom x_range if available
fig, _ = plot_summary_with_transitions(summary_df, edited_df, x_range=x_range)
st.pyplot(fig)
