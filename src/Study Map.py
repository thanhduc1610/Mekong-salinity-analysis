from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D


# ============================================================
# 1. FILE PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]
data_folder = PROJECT_ROOT / "Data" / "Raw"

vietnam_path = data_folder / "geoBoundaries-VNM-ADM1.geojson"
cambodia_path = data_folder / "geoBoundaries-KHM-ADM0.geojson"
river_path = data_folder / "HydroRIVERS_v10_as.gdb"


# ============================================================
# 2. LOAD DATA
# ============================================================

# Vietnamese provincial boundaries
provinces = gpd.read_file(vietnam_path)

# Cambodia national boundary
cambodia = gpd.read_file(cambodia_path)

# Asian river network
rivers = gpd.read_file(
    river_path,
    layer="HydroRIVERS_v10_as"
)


# ============================================================
# 3. PREPARE DATA
# ============================================================

# Vietnamese Mekong Delta provinces
# using administrative boundaries before the provincial mergers
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


# Study provinces
study_area = provinces[
    provinces["shapeName"].isin(["Cà Mau", "Kiên Giang"])
].copy()


# Convert spatial data to the same projected CRS
# WGS 84 / UTM Zone 48N
# Coordinates are in metres
mekong_delta = mekong_delta.to_crs(epsg=32648)
study_area = study_area.to_crs(epsg=32648)
cambodia = cambodia.to_crs(epsg=32648)
rivers = rivers.to_crs(epsg=32648)


# Map bounds
minx, miny, maxx, maxy = mekong_delta.total_bounds

padding_x = 50000  # 50 km
padding_y = 50000  # 50 km


# Crop Asian river network to the study-region map
rivers_vmd = rivers.cx[
    minx - padding_x : maxx + padding_x,
    miny - padding_y : maxy + padding_y
].copy()


# Keep only major rivers
major_rivers = rivers_vmd[
    rivers_vmd["ORD_STRA"] >= 6
].copy()


# ============================================================
# 4. PLOT MAP
# ============================================================

fig, ax = plt.subplots(figsize=(8, 7))


# ------------------------------------------------------------
# Cambodia
# ------------------------------------------------------------

cambodia.plot(
    ax=ax,
    facecolor="0.97",
    edgecolor="0.45",
    linewidth=0.5,
    zorder=1
)


# ------------------------------------------------------------
# Mekong Delta provinces
# ------------------------------------------------------------

mekong_delta.plot(
    ax=ax,
    facecolor="0.90",
    edgecolor="0.20",
    linewidth=0.6,
    zorder=2
)


# ------------------------------------------------------------
# Study provinces
# ------------------------------------------------------------

study_area.plot(
    ax=ax,
    facecolor="0.60",
    edgecolor="0.10",
    linewidth=0.8,
    zorder=3
)


# ------------------------------------------------------------
# Major rivers
# ------------------------------------------------------------

major_rivers.plot(
    ax=ax,
    color="0.35",
    linewidth=0.8,
    zorder=4
)


# ------------------------------------------------------------
# Study province labels
# ------------------------------------------------------------

for _, row in study_area.iterrows():

    point = row.geometry.representative_point()

    x = point.x
    y = point.y

    # Manually adjust Kiên Giang label
    if row["shapeName"] == "Kiên Giang":
        x -= 10000   # 10 km west
        y -= 20000   # 20 km south

    ax.text(
        x,
        y,
        row["shapeName"],
        ha="center",
        va="center",
        fontsize=9,
        fontweight="bold",
        color="black",
        zorder=5
    )


# ------------------------------------------------------------
# Cambodia label
# ------------------------------------------------------------

ax.text(
    0.16,
    0.82,
    "Cambodia",
    transform=ax.transAxes,
    fontsize=12,
    color="0.35",
    ha="center",
    va="center",
    zorder=5
)


# ------------------------------------------------------------
# North arrow
# ------------------------------------------------------------

# "N" label
ax.text(
    0.94,
    0.965,
    "N",
    transform=ax.transAxes,
    ha="center",
    va="center",
    fontsize=12,
    color="black",
    zorder=10
)

# North-pointing triangular arrowhead
ax.text(
    0.94,
    0.915,
    "▲",
    transform=ax.transAxes,
    ha="center",
    va="center",
    fontsize=16,
    color="black",
    zorder=10
)


# ------------------------------------------------------------
# Legend
# ------------------------------------------------------------

legend_elements = [

    Patch(
        facecolor="0.60",
        edgecolor="0.10",
        label="Study provinces\n(Cà Mau and Kiên Giang)"
    ),

    Patch(
        facecolor="0.90",
        edgecolor="0.20",
        label="Other Mekong Delta provinces"
    ),

    Patch(
        facecolor="0.97",
        edgecolor="0.45",
        label="Cambodia"
    ),

    Line2D(
        [0],
        [0],
        color="0.20",
        linewidth=0.8,
        label="Provincial boundary"
    ),

    Line2D(
        [0],
        [0],
        color="0.35",
        linewidth=2,
        label="Major rivers"
    )
]


ax.legend(
    handles=legend_elements,
    loc="lower right",
    fontsize=8,
    frameon=True,
    fancybox=False,
    framealpha=1,
    edgecolor="0.20",
    facecolor="white",
    handlelength=3,
    handleheight=1.5,
    borderpad=0.8,
    labelspacing=0.7
)


# ------------------------------------------------------------
# Map extent
# ------------------------------------------------------------

ax.set_xlim(
    minx - padding_x,
    maxx + padding_x
)

ax.set_ylim(
    miny - padding_y,
    maxy + padding_y
)


# ------------------------------------------------------------
# Final formatting
# ------------------------------------------------------------

ax.axis("off")

plt.tight_layout()

# IMPORTANT: only one plt.show()
plt.show()