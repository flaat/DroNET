import json
from src.simulation.configurator import Configurator
from ast import literal_eval as make_tuple


class MissionManager:
    def __init__(self):
        """
            path_from_json : whether generate or load the paths for the drones
            json_file : path to json file storing drone paths.
            A mission is defined as a dictionary storing for each drone a list of coordinates that represents hops in trajectories
            e.g.
            {
                0: [(1500, 0), (1637, 172), ... (1500, 0)],
                ...
                N: [(1500, 0), ...]
            }
        """
        # the constructor initially set an empty mission
        self.mission = {}
        self.config = Configurator().configuration

    def get_drone_path(self, drone_id: int):
        assert 0 <= drone_id < self.config.n_drones
        assert drone_id in self.mission.keys()
        return self.mission[drone_id]

    def set_drone_path(self, drone_id: int, path):
        assert 0 <= drone_id < self.config.n_drones
        self.is_path(path)
        self.mission[drone_id] = path

    def set_mission(self, mission):
        self.is_mission(mission)
        self.mission = mission

    def is_mission(self, mission):
        if type(mission) is not dict:
            assert False
        for drone_id, path in mission.items():
            if drone_id < 0 or drone_id >= self.config.n_drones: assert False
            self.is_path(path)

    def is_path(self, path):
        """
            Testing purposes only
            Return True if the path il well formatted, i.e. list of int tuple and each coordinate is within environment bounds
        """
        if type(path) is not list: assert False
        for hop_coord in path:
            if type(hop_coord) is not tuple: assert False
            if type(hop_coord[0]) is not int and type(hop_coord[1]) is not int: assert False
            if hop_coord[0] < 0 or hop_coord[1] < 0 or hop_coord[0] > self.config.env_width or hop_coord[
                1] > self.config.env_height: assert False

    def json_to_mission(self, json_file_in, whole=False):
        """
            This method loads the mission stored in json_file_in (must be a path)
            json files must be formatted as follows:
                {"drones":
                    [
                    {"index": "0", "tour": ["(1500, 0)", "(1637, 172)", ... (1500, 0)"]},
                    ...,
                    {"index": "N", "tour": ["(1500, 0)", ...]}
                    ]
                }
        """
        mission = {}
        with open(json_file_in, 'r') as in_file:
            data = json.load(in_file)
            for drone_data in data["drones"]:
                drone_index = int(drone_data["index"])
                if whole or drone_index < self.config.n_drones:
                    drone_path = []
                    for hop_coord in drone_data["tour"]:
                        coord = (int(hop_coord[0]), int(hop_coord[1]))
                        drone_path.append(coord)
                    mission[drone_index] = drone_path
        self.is_mission(mission)
        self.mission = mission

    def json_to_mission_old(self, json_file_in, whole=False):
        mission = {}
        with open(json_file_in, 'r') as in_file:
            data = json.load(in_file)
            for drone_data in data["drones"]:
                drone_index = int(drone_data["index"])
                if whole or drone_index < self.config.n_drones:
                    drone_path = []
                    for hop_coord in drone_data["tour"]:
                        coord = make_tuple(hop_coord)
                        drone_path.append(coord)
                    mission[drone_index] = drone_path
        return mission

    def mission_to_json(self, json_file_out):
        """
            This method stores the mission in json_file_out (must be a path)
        """

        with open(json_file_out, 'w') as out_file:
            paths = []
            for drone_id, path in self.mission.items():
                entry = {"index": drone_id, "tour": path}
                paths.append(entry)
            out_data = {"drones": paths}
            json.dump(out_data, out_file)

    def old_mission_format_to_new_format(self, file_in, file_out):
        self.mission = self.json_to_mission_old(file_in, True)
        self.mission_to_json(file_out)

    """ 
    
            #self.path_from_json = self.config.path_from_JSON
        #self.json_file = self.config.JSON_path_prefix.format(self.config.seed) # We assume json_file.format(seed) (?)

        #if self.path_from_json:
        #    self.path_dict = self.json_to_paths(self.json_file)
        #    self.rnd_paths = None
        #else:
        #    self.path_dict = None
        #    self.rnd_paths = np.random.RandomState(self.config.seed)

    def path(self, drone_id, simulator):
        takes the drone id and
            returns a path (list of tuple)
            for it.

            Notice that: the path can last
            less or more than the simulation.
            In the first case the path should be repeated.
        

        # TODO: invece che tutti questi booleani diversi in config, perche' non fare un enum?
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

    # TODO: perche' avere path hard coded quando posso caricarli da json.
    def __demo_path(self, drone_id):
        Add handcrafted torus here.
        tmp_path = {0: [(750, 750), (760, 750), (750, 750), (760, 750), (770, 750)],
                    1: [(1280, 80), (460, 1050), (1060, 1050), (1060, 450), (460, 450), (0, 1500)],
                    2: [(1320, 120), (460, 1050), (1060, 1050), (1060, 450), (460, 450), (0, 1500)],
                    3: [(1400, 160), (460, 1050), (1060, 1050), (1060, 450), (460, 450), (0, 1500)],
                    4: [(1500, 200), (460, 1050), (1060, 1050), (1060, 450), (460, 450), (0, 1500)]}
        return tmp_path[drone_id]
    """
