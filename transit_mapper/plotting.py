import os

import osmnx as ox
# import matplotlib.pyplot as plt


def plot_isochrones(isochrones, directory, filename, cmap="plasma"):
    """
    Plot multiple isochones. The isochrones must already by sorted from biggest 
    to smallest.
    """
    # TODO: sort based on bounding box
    widest_iso = isochrones[0]
    address, lat_lng = widest_iso.address, widest_iso.lat_lng

    # Filepath
    if filename is None:
        if address:
            street_address = address.split(",")[0].replace(" ", "_")
            filename = f"walking_isochrone_{street_address}.png"
        else:
            lon, lat = lat_lng[1], lat_lng[0]
            lon, lat = str(lon).replace(".","°"), str(lat).replace(".","°")
            filename = f"walking_isochrone_{lat}_{lon}.png"

    if not directory.exists():
        os.makedirs(directory)

    filepath = directory / filename

    # Color Scheme
    num_colors = len(isochrones)
    iso_colors = ox.plot.get_colors(num_colors, cmap=cmap, return_hex=True)

    # node_colors = {}
    edge_colors = {}

    for isochrone, color in zip(isochrones, iso_colors):
        # for node in isochrone.graph.nodes():
        #     node_colors[node] = color
        for edge in isochrone.graph.edges():
            edge_colors[edge] = color

    graph = widest_iso.graph
    # nc = [node_colors[node] if node in node_colors else 'none' for node in graph.nodes()]
    ec = [edge_colors[edge] if edge in edge_colors else 'none' for edge in graph.edges()]
    ns = [0 for _ in graph.nodes()]

    print(filepath)

    bgcolor="#262730"
    _, _ = ox.plot_graph(graph, edge_color=ec, node_size=ns,
        node_alpha=0.8, node_zorder=2, bgcolor=bgcolor, edge_linewidth=0.2,
        show=False, save=True, filepath=filepath, dpi=300)