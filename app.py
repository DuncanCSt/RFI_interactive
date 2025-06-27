import streamlit as st
import pandas as pd
import io

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

st.title("Simple RFI visualisation App")

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
# ``selected_rows`` may be returned as a list of dictionaries.  Convert it to a
# DataFrame so we can easily access the first selected row, if any.
if selected_rows is not None:
    selected_rows = pd.DataFrame(selected_rows)

    # Add a slider to select the zoom window around the selected frequency
    zoom_options = [0.1, 1, 10, 100]
    zoom_window = st.select_slider(
        "Zoom window (MHz)",
        options=zoom_options,
        value=1,
        help="Set the +/- MHz range around the selected frequency (log scale)"
    )

if selected_rows is not None and not selected_rows.empty:
    selected_frequency = selected_rows.iloc[0]["Frequency (MHz)"]
    # Define an x_range; for instance, +/- 5 around selected frequency:
    x_range = (selected_frequency - zoom_window, selected_frequency + zoom_window)
else:
    # Fallback, use full range or a default value
    x_range = (min(summary_df["frequency"]), max(summary_df["frequency"]))

# Update transitions_df with the edited score values and persist them
mask = transitions_df["Species"] == selected_value
transitions_df.loc[mask, "score"] = edited_df["score"].values
save_transitions_data(transitions_df)

# Add a button to reset x_range to None
if st.button("Reset x_range to full range"):
    x_range = (min(summary_df["frequency"]), max(summary_df["frequency"]))

# Plot results using the custom x_range if available
fig, _ = plot_summary_with_transitions(summary_df, edited_df, x_range=x_range)

# Only generate the PNG if the user clicks the "Prepare PNG" button.
if "png_buffer" not in st.session_state:
    st.session_state.png_buffer = None

if st.button("Prepare Plot for Download"):
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    st.session_state.png_buffer = buf.getvalue()
    st.success("Plot generated! Now click the download button below.")

# Only show the download button if the PNG has been generated.
if st.session_state.png_buffer is not None:
    st.download_button(
        label="Download plot as PNG",
        data=st.session_state.png_buffer,
        file_name="plot.png",
        mime="image/png",
    )

st.pyplot(fig)