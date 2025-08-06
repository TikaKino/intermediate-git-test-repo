import geopandas as gpd
from matplotlib.offsetbox import AnchoredText
import matplotlib.pyplot as plt
import pandas as pd


def plot_data(figure_name):
    '''
    plots a map of the data buoys found in the data/data_buoys.csv file.
    Uses data/north_atlantic.geojson as a boundary of the atlantic ocean.

    Parameters:
    figure_name (str): The name of the figure
    '''

    north_atlantic = gpd.read_file("data/north_atlantic.geojson")

    buoys = pd.read_csv("data/buoy_data.csv", keep_default_na=False, na_values=[""])

    locations = buoys[["Name", "latitude", "longitude"]]

    buoys_geo = gpd.GeoDataFrame(
        locations,
        geometry=gpd.points_from_xy(locations.longitude, locations.latitude),
        crs="EPSG:4326",
    )

    bounds = buoys_geo.total_bounds

    fig, ax = plt.subplots()
    ax.set_ylim([bounds[1] - 0.5, bounds[3] + 0.5])
    ax.set_xlim([bounds[0] - 0.5, bounds[2] + 0.5])
    north_atlantic.plot(ax=ax)

    buoys_geo.plot(ax=ax, color="red")

    axis_labels = []

    for buoy in buoys_geo.iterfeatures():
        ax.annotate(
            int(buoy["id"]) + 1,
            xy=(buoy["properties"]["longitude"], buoy["properties"]["latitude"]),
        )
        axis_labels.append(f"{int(buoy['id'])+1}: {buoy['properties']['Name']}")

    labels = AnchoredText(
        "\n".join(axis_labels),
        loc="lower left",
        prop=dict(size=8),
        frameon=True,
        bbox_to_anchor=(1.0, 0),
        bbox_transform=ax.transAxes,
    )
    labels.patch.set_boxstyle("round,pad=0.,rounding_size=0.2")
    ax.add_artist(labels)
    fig.tight_layout()
    fig.savefig(figure_name)


if __name__ == "__main__":
    plot_data("bouys_plot.png")
