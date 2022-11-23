import numpy as np
from math import inf
from src.routing_algorithms.BASE_routing import BASE_routing
from src.utilities.utilities import angle_between_points, euclidean_distance, projection_on_line_between_points

class GeoRouting(BASE_routing):

    def __init__(self, drone, simulator):
        BASE_routing.__init__(self, drone, simulator)

    def closest_to_sink(self, opt_neighbors: list):

        cur_pos = self.drone.coords
        depot_pos = self.drone.depot.coords
        # my_distance_to_depot = util.euclidean_distance(cur_pos, depot_pos)

        best_distance = euclidean_distance(cur_pos, depot_pos)
        best_drone = None

        for hello, neighbor in opt_neighbors:
            neighbor_pos = hello.cur_pos
            neighbor_distance_to_depot = euclidean_distance(neighbor_pos, depot_pos)
            # my_distance_to_neighbor = util.euclidean_distance(cur_pos, neighbor_pos)
            if (neighbor_distance_to_depot < best_distance):
                best_drone = neighbor
                best_distance = neighbor_distance_to_depot

        return best_drone

    def relay_selection(self, opt_neighbors: list):
        """
            STEP 1: implement NFP, MFP, CR and C2S considering the current position of d_0 (self.drone) and
                    the last known position of N(d_0) (drones in opt_neighbours)
            STEP 2: implement NFP, MFP, CR and C2S considering the next target position of d_0 and N(d_0)
            STEP 3: compare the performances of STEP1 and STEP2
            OPTIONAL: design and implement your own heuristic (you can consider all the info in the hello packets)
        """
        drone_to_route = self.closest_to_sink(opt_neighbors)

        return drone_to_route