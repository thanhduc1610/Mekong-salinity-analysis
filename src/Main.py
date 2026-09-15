from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parents[1]

file_path = (
    PROJECT_ROOT
    / "Data"
    / "Processed"
    / "Salinity measurements 2016"
    / "mb_hws_td_20160401_cleaned.csv"
)

df = pd.read_csv(file_path)

print(df.head())

# Reshape long data back into a matrix for the heatmap
salinity_matrix = df.pivot(
    index="depth_m",
    columns="distance_km",
    values="salinity_pss"
)

plt.figure(figsize=(12, 6))

plt.imshow(
    salinity_matrix,
    aspect="auto",
    origin="upper",
    extent=[
        salinity_matrix.columns.min(),
        salinity_matrix.columns.max(),
        salinity_matrix.index.max(),
        salinity_matrix.index.min()
    ]
)

plt.colorbar(label="Salinity (PSS)")

plt.xlabel("Distance upstream (km)")
plt.ylabel("Depth (m)")
plt.title("Salinity Profile – Dinh An, 1 April 2016")

plt.show()