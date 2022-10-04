import os
from pathlib import Path
from matplotlib.pyplot import plot

import osmnx as ox
import networkx as nx

from transit_mapper import graphs, plotting
from .isochrone import Isochrone


class TransitMapper:
    def __init__(self, data_directory=None, plots_directory=None, city=None):
        """
        TKTK
        """
        if data_directory is None:
            self.data_directory = Path(__file__).parent.parent
        else:
            self.data_directory = Path(data_directory)

        if plots_directory is None:
            self.plots_directory = self.data_directory / "plots"
        else:
            self.plots_directory = plots_directory

        self.city = city
        if city:
            if self.graph_path.exists():
                print("Citywide graph pickle file found. Will use that file.")
                self.citywide_graph = nx.read_gpickle(self.graph_path)
            else:
                self.download_citywide_graph(city)
        else:
            self.citywide_graph = None


    @property
    def graph_path(self):
        filename = self.city.replace(",", "").replace(" ","_").lower() + ".pkl"
        return self.data_directory / filename


    def download_citywide_graph(self, city, mode="walk", walking_speed=4.5):
        """
        Download a network graph for an entire place name
        """
        self.city = city
        graph = graphs.download_graph(city, mode=mode, walking_speed=walking_speed)
        nx.write_gpickle(graph, self.graph_path)
        self.citywide_graph = graph


    ########################## Walking Isochrone ##########################

    def walking_isochrone(self, trip_time=None, trip_times=None, 
                          address=None, lat_lng=None,
                          walking_speed=4.5,
                          filename=None):
        """
        Trace and plot walking isochrones for the location and times specified.
        Deafult walking speed of 4.5 km/hr.
        ---
        TKTK inputs.
        """
        # Trip Times
        if trip_time is None and trip_times is None:
            raise ValueError("Must specify either `trip_time` or `trip_times`.")
        elif trip_times is None:
            trip_times = [trip_time]
        trip_times = sorted(trip_times, reverse=True)

        # Sourch Graph
        if not graphs.location_in_city(self.citywide_graph, address=address, lat_lng=lat_lng):
            # Download a graph because this loation is either not in the 
            # citywide graph or there is no stored citywide graph
            source_graph = graphs.download_graph(address=address, lat_lng=lat_lng,
                mode="walk", walking_speed=walking_speed)
        else:
            source_graph = self.citywide_graph

        # Make Isochrones
        mode = "walk"
        if lat_lng is None:
            lat_lng = ox.geocode(address)
        kwargs = {
            "address":          address,
            "walking_speed":    walking_speed,
        }
        isochrones = [Isochrone(source_graph, lat_lng, trip_time, mode, **kwargs) for trip_time in trip_times]
        
        # Make Pretty
        plotting.plot_isochrones(isochrones, self.plots_directory, filename)

        


