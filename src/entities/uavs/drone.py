import numpy as np
from src.entities.depot.depots import Depot
from src.entities.events.event import Event
from src.entities.simulated_entities import Entity
from src.utilities import utilities
from src.simulation.configurator import Configurator


class Drone(Entity):

    def __init__(self, identifier: int, path: list, depot: Depot, clock, logger=None, network_dispatcher=None):

        super().__init__(identifier=identifier, clock=clock, logger=logger)

        self.coordinates = path[0]
        self.config = Configurator().configuration
        self.depot = depot
        self.path = path
        self.speed = self.config.drone_speed
        self.sensing_range = self.config.drone_sen_range
        self.communication_range = self.config.drone_com_range
        self.buffer_max_size = self.config.drone_max_buffer_size
        self.residual_energy = self.config.drone_max_energy
        self.come_back_to_mission = False
        self.last_move_routing = False

        # dynamic parameters
        self.tightest_event_deadline = None  # used later to check if there is an event that is about to expire
        self.current_waypoint = 0

        self.__buffer = []

        self.distance_from_depot = 0
        self.move_routing = False  # if true, it moves to the depot

        # setup drone routing algorithm
        self.routing_algorithm = self.config.routing_algorithm(self, network_dispatcher)
        # self.routing_algorithm = config.ROUTING_ALGORITHM.value(self, network_dispatcher)

        # last mission coord to restore the mission after movement
        self.last_mission_coords = None

    @property
    def all_packets(self):
        """
        Returns all the packets within the buffer
        @return: a list of packets or an empty list
        """

        return self.__buffer

    @property
    def buffer_length(self):
        """
        Returns the buffer length
        @return: an integer describing the current buffer length
        """

        return len(self.__buffer)

    @property
    def is_full(self):
        """
        Return True if the current buffer length is equal to the max length
        @return: True or False
        """

        return self.buffer_length == self.buffer_max_size

    def update_packets(self):
        """
        Removes the expired packets from the buffer
        @return:
        """

        temporary_buffer = []
        self.tightest_event_deadline = np.nan

        for packet in self.__buffer:

            if not packet.is_expired:

                # append again only if it is not expired
                temporary_buffer.append(packet)
                self.tightest_event_deadline = np.nanmin([self.tightest_event_deadline, packet.event_ref.deadline])

        self.__buffer = temporary_buffer

        if not self.buffer_length:

            self.move_routing = False

    def feel_event(self):
        """
        Feel a new event, and adds the packet relative to it, in its buffer.
        If the drones is doing movement the packet is not added in the buffer
        @return: None
        """

        generated_event = Event(coordinates=self.coordinates,
                                current_time=self.clock.current_time,
                                clock=self.clock)

        packet = generated_event.as_packet(self)

        if not self.move_routing and not self.come_back_to_mission:

            self.__buffer.append(packet)

        # store the events that are missing due to movement routing
        else:

            self.logger.add_event_not_listened(timestep=self.clock.current_time, event=generated_event)

    def accept_packets(self, packets):
        """
        Self drone adds packets of another drone, when it feels it passing by.
        @param packets:
        @return:
        """

        for packet in packets:

            # add if not notified yet, else don't, proprietary drone will delete all packets, but it is ok
            # because they have already been notified by someone already

            if not self.is_known_packet(packet):

                self.__buffer.append(packet)

    def routing(self, drones: list):
        """
        It Starts the routing process
        @param drones:
        @return:
        """

        self.distance_from_depot = utilities.euclidean_distance(self.depot.coordinates, self.coordinates)

        self.routing_algorithm.routing(drones)

    def move(self, time):
        """
        Move the drone to the next point if self.move_routing is false, else it moves towards the depot.
        time -> time_step_duration (how much time between two simulation frame)
        """
        if self.move_routing or self.come_back_to_mission:
            # metrics: number of time steps on active routing (movement) a counter that is incremented each time
            # drone is moving to the depot for active routing, i.e., move_routing = True
            # or the drone is coming back to its mission

            pass

        if self.move_routing:

            if not self.last_move_routing:  # this is the first time that we are doing move-routing

                self.last_mission_coords = self.coordinates

            self.__move_to_depot(time)

        else:

            if self.last_move_routing:  # I'm coming back to the mission

                self.come_back_to_mission = True

            self.__move_to_mission(time)

            # metrics: number of time steps on mission, incremented each time drone is doing sensing mission

        # set the last move routing
        self.last_move_routing = self.move_routing

    def is_known_packet(self, received_packet):
        """
        Returns True if drone has already a similar packet (i.e. a packet referred to the same event)
        @param received_packet:
        @return: True if the packet is known, False otherwise
        """

        for packet in self.__buffer:

            if packet.event_ref == received_packet.event_ref:

                return True

        return False

    def empty_buffer(self):
        """
        It cleans the buffer erasing all the packets within self.__buffer
        @return: None
        """

        self.__buffer = []

    def remove_packets(self, packets):
        """
        Removes the packets from the buffer.
        @param packets:
        @return:
        """

        for packet in packets:

            if packet in self.__buffer:

                self.__buffer.remove(packet)

                if self.config.debug:

                    print(f"Drone {str(self.identifier)} just removed packet {str(packet.identifier)}")

    def next_target(self):
        """
        This method returns the next coordinates for a Drone
        @return: a tuple of coordinates (x, y)
        """

        # case 1: if move_routing then go to the depot
        if self.move_routing:

            return self.depot.coordinates

        # case 2: if come_back_to_mission then go to the last coordinates known
        elif self.come_back_to_mission:

            return self.last_mission_coords

        # case 3: else go to the next waypoint in the path
        else:

            # if it reached the end of the path, start back to 0
            if self.current_waypoint >= len(self.path) - 1:

                return self.path[0]

            # else go to the next coordinates
            else:

                return self.path[self.current_waypoint + 1]

    def __move_to_mission(self, time):
        """
        When invoked the drone moves on the map.
        @param time: Time elapsed between two frames
        @return:
        """

        if self.current_waypoint >= len(self.path) - 1:

            self.current_waypoint = -1

        p0 = self.coordinates

        if self.come_back_to_mission:  # after move

            p1 = self.last_mission_coords

        else:

            p1 = self.path[self.current_waypoint + 1]

        all_distance = utilities.euclidean_distance(p0, p1)
        distance = time * self.speed

        if all_distance == 0 or distance == 0:

            self.__update_position(p1)

            return

        t = distance / all_distance

        if t >= 1:

            self.__update_position(p1)

        elif t <= 0:

            print("Error move drone, ratio < 0")
            exit(1)

        else:

            self.coordinates = (((1 - t) * p0[0] + t * p1[0]), ((1 - t) * p0[1] + t * p1[1]))

    def __update_position(self, p1):
        """

        @param p1:
        @return:
        """
        if self.come_back_to_mission:

            self.come_back_to_mission = False
            self.coordinates = p1

        else:

            self.current_waypoint += 1
            self.coordinates = self.path[self.current_waypoint]

    def __move_to_depot(self, time):
        """
        When invoked the drone moves to the depot.
        @param time: Time elapsed between two frames
        @return:
        """

        p0 = self.coordinates
        p1 = self.depot.coordinates
        all_distance = utilities.euclidean_distance(p0, p1)
        distance = time * self.speed

        if all_distance == 0:

            self.move_routing = False

            return

        t = distance / all_distance

        if t >= 1:

            # with the next step you would surpass the target
            self.coordinates = p1

        elif t <= 0:

            print("Error routing move drone, ratio < 0")
            exit(1)

        else:

            self.coordinates = (((1 - t) * p0[0] + t * p1[0]), ((1 - t) * p0[1] + t * p1[1]))

    def __repr__(self):
        """

        @return:
        """

        return f"Drone {str(self.identifier)}"

    def __hash__(self):
        return hash(self.identifier)


