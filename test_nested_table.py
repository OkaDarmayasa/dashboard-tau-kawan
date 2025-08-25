import streamlit as st
import pandas as pd
from st_aggrid import GridOptionsBuilder, AgGrid

# Example data
data = {
    "No_LHP": ["LHP1"] * 18,
    "temuan": ["T1"]*6 + ["T2"]*6 + ["T3"]*6,
    "rekomendasi": ["R1"]*3 + ["R2"]*3 + ["R1"]*3 + ["R2"]*3 + ["R1"]*3 + ["R2"]*3,
    "rencana_aksi": [f"A{i}" for i in range(1, 19)]
}
df = pd.DataFrame(data)

# Configure grid
gb = GridOptionsBuilder.from_dataframe(df)

# Default column behavior
gb.configure_default_column(groupable=True, enableRowGroup=True, aggFunc="count")

# Force grouping from left to right
gb.configure_column("No_LHP", rowGroup=True, hide=True)
gb.configure_column("temuan", rowGroup=True, hide=True)
gb.configure_column("rekomendasi", rowGroup=True, hide=True)

# Let rencana_aksi remain visible
gb.configure_column("rencana_aksi")

# Enable sidebar & grouping display style
gb.configure_side_bar()
gb.configure_grid_options(groupDisplayType="multipleColumns")

grid_options = gb.build()

AgGrid(
    df,
    gridOptions=grid_options,
    enable_enterprise_modules=True,
    update_mode="MODEL_CHANGED",
)
