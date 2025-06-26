import pandas as pd
from st_aggrid import (
    AgGrid,
    GridOptionsBuilder,
    GridUpdateMode,
    DataReturnMode,
    JsCode,
)


def editable_transitions_table(df: pd.DataFrame) -> dict:
    """Display an editable AG Grid table for df and return the grid response dict."""
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
        update_mode=GridUpdateMode.VALUE_CHANGED,
        data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
        allow_unsafe_jscode=True,
    )
    return grid_response
