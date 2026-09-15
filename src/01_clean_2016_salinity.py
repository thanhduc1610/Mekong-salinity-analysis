from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]

data_folder = (PROJECT_ROOT/ "Data"/ "Raw"/ "Salinity measurements in the Mekong Delta")

output_folder = (PROJECT_ROOT/ "Data"/ "Processed"/ "Salinity measurements 2016")

# Create the folder if it doesn't already exist
output_folder.mkdir(parents=True, exist_ok=True)

# Create the folder if it doesn't already exist
output_folder.mkdir(parents=True, exist_ok=True)

# Find every .txt file in the folder
txt_files = list(data_folder.glob("*.txt"))

# for file_path in txt_files:
#     print(file_path.name)

all_data = [] #initiate a list for file names in directory

for file_path in txt_files:

    # Read one file
    df = pd.read_csv(file_path, comment="#", header=None)

    # Label columns: every 3 km upstream
    df.columns = [i * 3 for i in range(df.shape[1])]

    # Label rows: every 0.5 m depth
    df.index = [i * 0.5 for i in range(df.shape[0])]

    # Name axes
    df.index.name = "depth_m"
    df.columns.name = "distance_km"

    # Convert wide to long
    df_long = (
        df.reset_index()
          .melt(
              id_vars="depth_m",
              var_name="distance_km",
              value_name="salinity_pss"
          )
    )

    # Keep track of which file these measurements came from
    df_long["source_file"] = file_path.name

    # Create output filename based on original filename
    output_file = output_folder / f"{file_path.stem}_cleaned.csv"

    # Save cleaned dataframe
    df_long.to_csv(output_file, index=False)

    print(f"Saved: {output_file.name}")