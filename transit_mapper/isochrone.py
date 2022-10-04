import networkx as nx

from transit_mapper import graphs


class Isochrone:
    def __init__(self, source_graph, lat_lng, trip_time, mode, **kwargs):
        self.source_graph = source_graph
        self.lat_lng = lat_lng
        self.trip_time = trip_time
        self.mode = mode

        # Keyword Arguments
        for key, value in kwargs.items():
            setattr(self, key, value)
        
        # Graph Attributes
        self.graph = self.trace_subgraph()
        self.set_graph_attributes()
        
        # TODO: set default speeds
        # Walking & Transit
        self.walking_speed = None
        self.transit_frequency_scale = 1.0
        self.transit_bus_speed_scale = 1.0

        # Driving
        # self.congestion_factor = 1.0

        # Biking
        # self.biking_speed = None


    def trace_subgraph(self):
        center_node = graphs.nearest_node(self.source_graph, self.lat_lng)
        subgraph = nx.ego_graph(self.source_graph, center_node, 
                        distance=f"{self.mode}_time",
                        radius=self.trip_time)
        return subgraph


    def set_graph_attributes(self):
        self.bounds = None
        self.shape = None


    def union(self, isochrone):
        """
        Update this isocrhone to be the 
        """
        pass