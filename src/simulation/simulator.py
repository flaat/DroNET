import json
from dataclasses import asdict
from src.utilities.EventGenerator import EventGenerator
from src.utilities.PathManager import PathManager
from src.drawing import pp_draw
from src.entities.depot.depots import Depot
from src.entities.environment.environment import Environment
from src.entities.uavs.drone import Drone
from src.simulation.logger import Logger
from src.simulation.metrics import Metrics
from src.utilities import utilities
from src.routing_algorithms.net_routing import MediumDispatcher
from tqdm import tqdm
from src.simulation.configurator import Configurator

import numpy as np
import time

"""
This file contains the Simulation class. It allows to specify all the relevant parameters of the simulation,
by default all the parameters are set to be those in the config file. For extensive experimental campains, 
you can initialize the Simulator with non default values. 
"""


class Simulator:

    def __init__(self):

        # Get config from configurator object
        self.config = Configurator().configuration

        self.sim_save_file = self.config.save_plot_dir + self.__sim_name()

        self.clock = Clock()

        # Setting up metrics and logger dataclasses
        self.metrics = Metrics()
        self.logger = Logger()

        # Setting up the simulation
        self.__set_simulation()

        # TODO: make simulation name configurable

        date_and_time = str(time.strftime("%d%m%Y-%H%M%S"))
        self.simulation_name = "test-" + date_and_time + "_" + str(self.config.simulation_name) + "_" + str(self.config.seed)
        self.simulation_test_dir = self.simulation_name + "/"

        self.event_generator = EventGenerator()

    def __set_random_generators(self):
        """
        Sets a random state for each component based on the seed.
        @return:
        """
        if self.config.seed is not None:
            self.rnd_network = np.random.RandomState(self.config.seed)
            self.rnd_routing = np.random.RandomState(self.config.seed)
            self.rnd_env = np.random.RandomState(self.config.seed)
            self.rnd_event = np.random.RandomState(self.config.seed)

    def __set_simulation(self):
        """
        Method initializes many elements needed for the simulation, like depot and drones. It also checks
        if the simulation needs to be rendered or not.
        @return:
        """

        self.network_dispatcher = MediumDispatcher(self)

        self.__set_random_generators()

        self.path_manager = PathManager(path_from_json=self.config.path_from_JSON,
                                                  json_file=self.config.JSON_path_prefix,
                                                  seed=self.config.seed)

        self.environment = Environment(width=self.config.env_width,
                                       height=self.config.env_height)

        self.depot = Depot(coordinates=self.config.depot_coordinates,
                           communication_range=self.config.depot_com_range,
                           clock=self.clock,
                           logger=self.logger)

        self.drones = []

        # drone 0 is the first
        for i in range(self.config.n_drones):
            self.drones.append(Drone(identifier=i,
                                     path=self.path_manager.path(i, self),
                                     depot=self.depot,
                                     network_dispatcher=self.network_dispatcher,
                                     clock=self.clock,
                                     logger=self.logger))

        self.environment.drones = self.drones
        self.environment.depot = self.depot

        # Set the maximum distance between the drones and the depot
        self.max_dist_drone_depot = utilities.euclidean_distance(self.depot.coordinates,
                                                                 (self.config.env_width,
                                                                  self.config.env_height))

        if self.config.show_plot or self.config.save_plot:
            self.draw_manager = pp_draw.PathPlanningDrawer(env=self.environment,
                                                           padding=25,
                                                           borders=True)
    # TODO: useful?
    def __sim_name(self) -> str:
        """
        Returns the identification name for
        the current simulation. It is useful to print
        the simulation progress
        @return: str
        """

        return f"SIMULATION_SEED: {str(self.config.seed)} drones: {str(self.config.n_drones)} "

    def __plot(self):
        """
        renders all the components of the simulation the screen, namely the drones, depot and relative labels.
        @return:
        """

        if self.cur_step % self.config.skip_simulation_step != 0:
            return

        # delay draw
        if self.config.wait_simulation_step > 0:
            time.sleep(self.config.wait_simulation_step)

        # drones plot
        for drone in self.drones:
            self.draw_manager.draw_drone(drone=drone)

        # depot plot
        self.draw_manager.draw_depot(self.depot)

        # events
        for event in self.environment.active_events:
            self.draw_manager.draw_event(event)

        # draw simulation info
        self.draw_manager.draw_simulation_info(cur_step=self.cur_step, max_steps=self.config.simulation_length)

        # rendering phase
        file_name = self.sim_save_file + str(self.cur_step) + ".png"
        # TODO: python fails if SAVE_PLOT flag is set to True.
        self.draw_manager.update(show=self.config.show_plot, save=self.config.save_plot, filename=file_name)


    def run(self):
        """
        the method starts the simulation
        """

        for cur_step in tqdm(range(self.config.simulation_length)):

            self.clock.next_time_step()

            self.cur_step = cur_step
            # check for new events and remove the expired ones from the environment
            # self.environment.update_events(cur_step)
            # sense the area and move drones and sense the area
            self.network_dispatcher.run_medium(cur_step)

            # generates events
            # sense the events
            self.event_generator.handle_events_generation(cur_step, self.drones)

            for drone in self.drones:
                # 1. update expired packets on drone buffers
                # 2. try routing packets vs other drones or depot
                # 3. actually move the drone towards next waypoint or depot

                drone.update_packets()
                drone.routing(self.drones)
                drone.move(self.config.time_step_duration)

            if self.config.show_plot or self.config.save_plot:
                self.__plot()

        if self.config.debug:
            print("End of simulation, sim time: " + str(
                (self.cur_step + 1) * self.config.time_step_duration) + " sec, #iteration: " + str(self.cur_step + 1))

    def close(self):
        """
        Computes, prints and saves all the metrics relative to the simulation.
        @return:
        """
        print("Closing simulation")
        logs_path = "data/logs"

        self.logger.write(path=logs_path, filename=self.simulation_name)
        self.compute_final_metrics()
        self.print_metrics(metrics=True, logger=False)
        self.save_metrics(self.config.root_evaluation_delta + self.simulation_name)

    def compute_final_metrics(self):
        """
        Computes some metrics that will be useful to the user once the simulation ends.
        @return:
        """
        # TODO: why is this here if by default the logger is not printed in the print_metrics function?

        delivery_time_list = []

        # TODO: why make the delivery_time variable? just .append(calculation)
        for timestep, source_drone, packet in self.logger.drones_packets_to_depot:
            delivery_time = packet.time_delivery - packet.time_step_creation
            delivery_time_list.append(delivery_time)

        self.metrics.packet_mean_delivery_time = sum(delivery_time_list) / len(delivery_time_list)

        self.metrics.drones_packets_to_depot = len(self.logger.drones_packets_to_depot)
        self.metrics.all_packets_correctly_sent_by_drones = len(self.logger.drones_packets)

    def print_metrics(self, metrics: bool = True, logger: bool = False):
        """
        Prints the contents of metrics or logger classes.
        @return:
        """
        if metrics:
            print(self.metrics)

        if logger:
            print(self.logger)

    # TODO: self.metrics.save(...) does not exist, implement or remove?

    def save_metrics(self, filename_path, save_pickle=False):
        """
            function logs all metrics in files either in .json or .pickle format.
        """
        self.metrics.save_as_json(filename_path + ".json")
        if save_pickle:
            self.metrics.save(filename_path + ".pickle")


class Clock:

    def __init__(self):
        self._current_time = -1

    @property
    def current_time(self):
        """
        Returns the current time
        @return:
        """

        return self._current_time

    @current_time.setter
    def current_time(self, a):
        """

        @param a:
        @return:
        """

        raise Exception("It is not possible to modify the current time")

    def next_time_step(self):
        """

        @return:
        """

        self._current_time += 1
