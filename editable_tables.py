import pandas as pd
from st_aggrid import (
    AgGrid,
    GridOptionsBuilder,
    GridUpdateMode,
    DataReturnMode,
    JsCode,
)


def editable_transitions_table(df: pd.DataFrame) -> dict:
    """Return a grid widget whose edits and row selections trigger a rerun."""
    row_style = JsCode(
        """
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
"""
    )

    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_column(
        "score",
        editable=True,
        cellEditor="agSelectCellEditor",
        cellEditorParams={"values": ["fully clean", "partially clean", "not clean"]},
    )
    gb.configure_grid_options(
        getRowStyle=row_style,
    )
    # Enable single row selection
    gb.configure_selection("single")
    grid_options = gb.build()

    grid_response = AgGrid(
        df,
        gridOptions=grid_options,
        # Trigger a rerun whenever either a cell edit or a row selection
        # modifies the underlying grid model.  ``MODEL_CHANGED`` captures
        # both VALUE_CHANGED and SELECTION_CHANGED events so the app reacts
        # immediately to row selections.
        update_mode=GridUpdateMode.MODEL_CHANGED,
        data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
        allow_unsafe_jscode=True,
    )
    return grid_response
