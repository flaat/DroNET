import numpy as np
import json
from src.simulation.configurator import Configurator
from src.utilities import random_waypoint_generation
from src.utilities import formulas
from ast import literal_eval as make_tuple


def json_to_paths(json_file_path):
    """ load the tour for drones
        and return a dictionary {drone_id : list of waypoint}

        e.g.,
        accept json that contains:
        {"drones": [{"index": "0", "tour": ["(1500, 0)", "(1637, 172)", ...
                    (1500, 0)"]}, {"index": "1", "tour": ["(1500, 0)",

        TOURS = {
            0 : [(0,0), (2000,2000), (1500, 1500), (200, 2000)],
            1 : [(0,0), (2000, 200), (200, 2000), (1500, 1500)]
        }
    """
    out_data = {}
    with open(json_file_path, 'r') as in_file:
        data = json.load(in_file)
        for drone_data in data["drones"]:
            drone_index = int(drone_data["index"])
            drone_path = []
            for waypoint in drone_data["tour"]:
                drone_path.append(make_tuple(waypoint))
            out_data[drone_index] = drone_path
    return out_data


class PathManager:

    def __init__(self, path_from_json: bool, json_file: str, seed: int):
        """
            path_from_json : wheter generate or load the paths for the drones
            json file to read for take the paths of drones
            We assume json_file.format(seed)
        """
        self.config = Configurator().configuration
        self.path_from_json = path_from_json
        self.json_file = json_file.format(seed)
        if path_from_json:
            self.path_dict = json_to_paths(self.json_file)
            self.rnd_paths = None
        else:
            self.path_dict = None
            self.rnd_paths = np.random.RandomState(seed)

    def path(self, drone_id, simulator):
        """ takes the drone id and
            returns a path (list of tuple)
            for it.

            Notice that: the path can last
            less or more than the simulation.
            In the first case the path should be repeated.
        """
        if self.config.demo_path:  # some demo paths
            return self.__demo_path(drone_id)
        if self.config.circle_path:
            return self.__cirlce_path(drone_id, simulator)
        elif self.path_from_json:  # paths from loaded json
            return self.path_dict[drone_id]
        else:  # generate dynamic paths
            return random_waypoint_generation.get_tour(self.config.drone_max_energy, self.config.env_width,
                                                       self.config.depot_coordinates,
                                                       random_generator=self.rnd_paths,
                                                       range_decision=self.config.random_steps,
                                                       random_starting_point=self.config.random_start_point)

    def __cirlce_path(self, drone_id, simulator, center=None, radius=None):
        if center is None:
            center = simulator.depot_coordinates
        if radius is None:
            radius = simulator.depot_com_range - 10
        n_drones = simulator.n_drones
        traj = formulas.compute_circle_path(radius, center)
        step_start = int(len(traj) / n_drones)
        return traj[(drone_id * step_start):] + traj[:(drone_id * step_start)]

    def __demo_path(self, drone_id):
        """ Add handcrafted torus here.  """
        tmp_path = {0: [(750, 750), (760, 750), (750, 750), (760, 750), (770, 750)],
                    1: [(1280, 80), (460, 1050), (1060, 1050), (1060, 450), (460, 450), (0, 1500)],
                    2: [(1320, 120), (460, 1050), (1060, 1050), (1060, 450), (460, 450), (0, 1500)],
                    3: [(1400, 160), (460, 1050), (1060, 1050), (1060, 450), (460, 450), (0, 1500)],
                    4: [(1500, 200), (460, 1050), (1060, 1050), (1060, 450), (460, 450), (0, 1500)]}
        return tmp_path[drone_id]
