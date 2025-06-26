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
selected_value = st.sidebar.selectbox("Select Transition Type", transition_types)
filtered_transitions_df = transitions_df[transitions_df["Species"] == selected_value].copy()

# Display editable table and get updated values
edited_df = editable_transitions_table(filtered_transitions_df)

# Update ``transitions_df`` with the edited ``score`` values and persist them
mask = transitions_df["Species"] == selected_value
transitions_df.loc[mask, "score"] = edited_df["score"].values
save_transitions_data(transitions_df)

# Plot results
fig, _ = plot_summary_with_transitions(summary_df, edited_df)
st.pyplot(fig)
