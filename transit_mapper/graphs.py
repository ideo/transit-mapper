import osmnx as ox


def download_graph(city=None, address=None, lat_lng=None, mode="walk",  
                   time_radius=60, walking_speed=4.5):
    """
    Download a walking graph from the provided location.

    For now, assumes walking at a speed of 4.5 km/hr.

    TODO: Driving and Biking too
    """

    # How far you can travel in a straight line, in meters
    meters_per_minute = walking_speed / 60 * 1000
    radius = time_radius * meters_per_minute

    if city:
        graph = download_graph_from_place_name(city, mode=mode)
    elif address:
        graph = download_graph_from_address(address, radius, mode=mode)
    elif lat_lng:
        graph = download_graph_from_lat_lng(address, radius, mode=mode)
    else:
        raise ValueError("Must specify a starting location or city name.")

    graph = add_travel_times_to_graph(graph, meters_per_minute, mode)
    return graph


def download_graph_from_place_name(name, mode="walk"):
    print(f"Downloading the citywide network graph for {name}.")
    graph = ox.graph_from_place(name,
            network_type=mode,
            retain_all=False,
            truncate_by_edge=True,
            simplify=True)
    print("✓")
    return graph


def download_graph_from_address(address, radius, mode="walk"):
    """
    4.5 km/hr is the default walking speed, so this downloads the graph 
    that is walkable in one hour.
    ---
        radius (int):   graph radius in meters
        mode (str):     network type 
    """
    print(f"Downloading graph surrounding {address}.")
    graph, lat_lng = ox.graph_from_address(address, 
        dist=radius, 
        network_type=mode,
        return_coords=True,
        truncate_by_edge=True,
        simplify=True)
    print("✓")
    # return graph, lat_lng
    return graph


def download_graph_from_lat_lng(lat_lng, radius, mode="walk"):
    print(f"Downloading graph surrounding {lat_lng}.")
    graph = ox.graph_from_point(lat_lng, 
        dist=radius, 
        network_type=mode,
        return_coords=True,
        truncate_by_edge=True,
        simplify=True)
    print("✓")
    return graph


def add_travel_times_to_graph(graph, speed, mode):
        """
        Update edge data with the travels times for each mode.
        """
        # TODO: Check if the edge is a walking path or not. Only add walking 
        # speed to walking graph.
        for _, _, _, data in graph.edges(data=True, keys=True):
            # data['travel_time'] = data['length'] / speed
            data[f"{mode}_time"] = data['length'] / speed
        return graph


def location_in_city(citywide_graph, address=None, lat_lng=None):
    if citywide_graph is None:
        return False

    if address:
        lat_lng = ox.geocode(address)

    # Is this point within the graph?
    lon, lat = lat_lng[1], lat_lng[0]
    nearest_node = ox.distance.nearest_nodes(citywide_graph, lon, lat)
    if not isinstance(nearest_node, int):
        nearest_node = nearest_node[0]
    node_lat = citywide_graph.nodes[nearest_node]["y"]
    node_lon = citywide_graph.nodes[nearest_node]["x"]

    threshold = 0.0008
    if abs(node_lat-lat) < threshold and abs(node_lon-lon) < threshold:
        return True
    else:
        return False


def nearest_node(graph, lat_lng):
    lon, lat = lat_lng[1], lat_lng[0]
    nearest_node = ox.distance.nearest_nodes(graph, lon, lat)

    # If there are multiple equidistance nodes, just take the first one
    if not isinstance(nearest_node, int):
        nearest_node = nearest_node[0]

    return nearest_node