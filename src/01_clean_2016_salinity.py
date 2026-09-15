from pathlib import Path
import pandas as pd

# Project root: Mekong/
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Data file
file_path = (
    PROJECT_ROOT
    / "Data"
    / "Raw"
    / "Salinity measurements in the Mekong Delta"
    / "mb_hws_da_20160401.txt"
)

df = pd.read_csv(file_path, comment="#", header=None)
df.columns = [i * 3 for i in range(df.shape[1])] #create labels for columns for every 3km increment upstream
df.index = [i * 0.5 for i in range(df.shape[0])] #create labels for rows for every 0.5m increment in depth

# Name the axes
df.index.name = "depth_m"
df.columns.name = "distance_km"

# Convert from wide format to long format
df_long = (df.reset_index().melt(id_vars="depth_m",var_name="distance_km",value_name="salinity_pss"))

print(df_long.head(10))
print(df_long.shape)