import numpy as np
import src.utilities.utilities as util

from src.routing_algorithms.BASE_routing import BASE_routing


class GeoRoutingStud(BASE_routing):
    def __init__(self, drone, simulator):
        BASE_routing.__init__(self, drone, simulator)

    def relay_selection(self, opt_neighbors, packet):
        """
            STEP 1: implement NFP, MFP, CR and C2S considering the current position of d_0 (self.drone) and
                    the last known position of N(d_0) (drones in opt_neighbours)
            STEP 2: implement NFP, MFP, CR and C2S considering the next target position of d_0 and N(d_0)
            STEP 3: compare the performances of STEP1 and STEP2
            OPTIONAL: design and implement your own heuristic (you can consider all the info in the hello packets)
        """
        self_coords, depot_coords = self.drone.coords, self.drone.depot.coords
        
        """
        Alex note:
        L'ultimo opzionale parametro booleano serve a specificare se si vogliono usare i target dei droni o meno
        """
        #return CS2(self, opt_neighbors, depot_coords, self_coords)
        return closest_to_sink(self, opt_neighbors)
        # return CS2(self, opt_neighbors, depot_coords, True)
        # return MFP(self, opt_neighbors, self_coords, depot_coords)
        # return MFP(self, opt_neighbors, self_coords, depot_coords, True)
        # return CR(self, opt_neighbors, self_coords, depot_coords)
        # return CR(self, opt_neighbors, self_coords, depot_coords, True)
        # return NFP(self, opt_neighbors, self_coords, depot_coords)
        #return NFP(self, opt_neighbors, self_coords, depot_coords, True)    


def CS2(self, opt_neighbors: list, depot_coords, self_coords, target=False):
    distances = []

    if target:
        for hello, _ in opt_neighbors:
            eu_dist = util.euclidean_distance(hello.next_target, depot_coords)
            distances.append(eu_dist)
    else:
        for _, n_drone in opt_neighbors:
            eu_dist = util.euclidean_distance(n_drone.coords, self.drone.depot.coords)
            distances.append(eu_dist)

    distances.append(util.euclidean_distance(self_coords, self.drone.depot.coords))
    idx_drone = np.argmin(distances)

    if idx_drone == len(distances)-1:
        return None

    return opt_neighbors[idx_drone][1]

def closest_to_sink(self, opt_neighbors: list):

        cur_pos = self.drone.coords
        depot_pos = self.drone.depot.coords
        # my_distance_to_depot = util.euclidean_distance(cur_pos, depot_pos)

        best_distance = util.euclidean_distance(cur_pos, depot_pos)
        best_drone = None

        for hello, neighbor in opt_neighbors:
            neighbor_pos = hello.cur_pos
            neighbor_distance_to_depot = util.euclidean_distance(neighbor_pos, depot_pos)
            # my_distance_to_neighbor = util.euclidean_distance(cur_pos, neighbor_pos)
            if (neighbor_distance_to_depot < best_distance):
                best_drone = neighbor
                best_distance = neighbor_distance_to_depot

        return best_drone

def MFP(self, opt_neighbors: list, self_coords, depot_coords, target=False):
    projections = []
    if target:
        for hello, _ in opt_neighbors:
            mfp = util.projection_on_line_between_points(self.drone.next_target(), depot_coords, hello.next_target)
            projections.append(mfp)
    else:
        for _, n_drone in opt_neighbors:
            mfp = util.projection_on_line_between_points(self_coords, depot_coords, n_drone.coords)
            projections.append(mfp)
    idx_drone = np.argmax(projections)

    return opt_neighbors[idx_drone][1]

def CR(self, opt_neighbors: list, self_coords, depot_coords, target=False):
    projections = []
    if target:
        for hello, _ in opt_neighbors:
            cr = util.angle_between_points(self.drone.next_target(), depot_coords, hello.next_target)
            projections.append(cr)
    else:
        for _, n_drone in opt_neighbors:
            cr = util.angle_between_points(self_coords, depot_coords, n_drone.coords)
            projections.append(cr)

    idx_drone = np.argmin(projections)
    return opt_neighbors[idx_drone][1]

def NFP(self, opt_neighbors: list, self_coords, depot_coords, target=False):
    projections = []
    if target:
        for hello, _ in opt_neighbors:
            nfp = util.projection_on_line_between_points(self.drone.next_target(), depot_coords, hello.next_target)
            projections.append(nfp)
    else:
        for _, n_drone in opt_neighbors:
            nfp = util.projection_on_line_between_points(self_coords, depot_coords, n_drone.coords)
            projections.append(nfp)

    idx_drone = np.argmin(projections)
    return opt_neighbors[idx_drone][1]