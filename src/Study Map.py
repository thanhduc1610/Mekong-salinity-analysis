from pathlib import Path
import geopandas as gpd
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parents[1]

data_folder = PROJECT_ROOT / "Data" / "Raw"

data_path = data_folder / "geoBoundaries-VNM-ADM1.geojson"

# print(data_path)
# print(data_path.exists())

provinces = gpd.read_file(data_path) #read in data from geojson file

# print(provinces.columns)
# print(provinces.crs)
# print(provinces.head())

# print(
#     provinces[
#         provinces["shapeName"].str.contains(
#             "Mau|Giang",
#             case=False,
#             na=False
#         )
#     ]["shapeName"]
# )

#create study area subset
study_area = provinces[
    provinces["shapeName"].isin(["Cà Mau", "Kiên Giang"])
].copy()

# print(study_area["shapeName"])

#rough visualization
# fig, ax = plt.subplots(figsize=(7, 10))

# All Vietnamese Mekong Delta provinces before merger of provinces
mekong_names = [
    "An Giang",
    "Bạc Liêu",
    "Bến Tre",
    "Cà Mau",
    "Cần Thơ",
    "Đồng Tháp",
    "Hậu Giang",
    "Kiên Giang",
    "Long An",
    "Sóc Trăng",
    "Tiền Giang",
    "Trà Vinh",
    "Vĩnh Long"
]

mekong_delta = provinces[
    provinces["shapeName"].isin(mekong_names)
].copy()

print(mekong_delta["shapeName"].sort_values())
print("Number selected:", len(mekong_delta))


# add a projected CRS with coordinates in meters
mekong_delta = mekong_delta.to_crs(epsg=32648)
study_area = study_area.to_crs(epsg=32648)

# print(mekong_delta.crs)

#Cambodia
cambodia_path = data_folder / "geoBoundaries-KHM-ADM0.geojson"

cambodia = gpd.read_file(cambodia_path)

print(cambodia.crs)
cambodia = cambodia.to_crs(epsg=32648)

fig, ax = plt.subplots(figsize=(8, 7))

# Cambodia as geographic context
cambodia.plot(
    ax=ax,
    facecolor="whitesmoke",
    edgecolor="gray",
    linewidth=0.5
)

# Mekong Delta plot
mekong_delta.plot(
    ax=ax,
    facecolor="lightgray",
    edgecolor="black",
    linewidth=0.6
)

# Study provinces
study_area.plot(
    ax=ax,
    facecolor="orange",
    edgecolor="black",
    linewidth=0.8
)

# Province labels
for _, row in mekong_delta.iterrows():
    point = row.geometry.representative_point()

    ax.text(
        point.x,
        point.y,
        row["shapeName"],
        ha="center",
        va="center",
        fontsize=8
    )

# Set map extent around the Mekong Delta
minx, miny, maxx, maxy = mekong_delta.total_bounds

padding_x = 50000
padding_y = 50000

ax.set_xlim(minx - padding_x, maxx + padding_x)
ax.set_ylim(miny - padding_y, maxy + padding_y)

ax.axis("off")
plt.show()