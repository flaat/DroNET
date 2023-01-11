from src.entities.simulated_entities import Entity
from src.plots import config
from src.utilities import utilities


class Packet(Entity):
    """
    A packet is an entity generated by an event in the Area-of-Interest.
    """

    def __init__(self, clock, event_ref=None):
        """
        @param simulator:
        @param event_ref:
        """

        # id(self) is the id of this instance (unique for every new created packet),
        # the coordinates are those of the event
        super().__init__(identifier=id(self), clock=clock)

        self.__TTL = -1  # TTL is the number of hops that the packet crossed
        self.__max_TTL = 1000
        self.time_step_creation = clock.current_time
        self.event_ref = event_ref
        self.number_retransmission_attempt = 0
        self.last_2_hops = []

        self.optional_data = None  # list
        self.time_delivery = None

        # if the packet was sent with move routing or not
        self.is_move_packet = None

    @property
    def is_expired(self):
        """
        A Packet expires if the deadline of the event expires, or the maximum TTL is reached
        @return: True if the packet is expired False otherwise
        """

        return self.clock.current_time - self.time_step_creation > self.__max_TTL

    def to_json(self):
        """ return the json repr of the obj """

        return {"i_gen": self.time_step_creation,
                "i_dead": self.event_ref.deadline,
                "id": self.identifier,
                "TTL": self.__TTL,
                "id_event": self.event_ref.identifier}

    def add_hop(self, drone):
        """
        Add a new hop in the packet last_2_hops list
        @param drone:
        @return:
        """

        if len(self.last_2_hops) == 2:

            # keep just the last two HOPS
            self.last_2_hops = self.last_2_hops[1:]

        self.last_2_hops.append(drone)
        self.increase_ttl_hops()

    def increase_ttl_hops(self):
        """
        @return:
        """

        self.__TTL += 1

    def __repr__(self):

        packet_type = str(self.__class__).split(".")[-1].split("'")[0]

        # TODO: do we care about coordinates?
        # return f"{packet_type} id: {str(self.identifier)} event id: {str(self.event_ref.identifier)} coordinates: {str(self.coordinates)}"


class DataPacket(Packet):
    """
    A DataPacket, up to now it is not very different from a Packet...
    """

    def __init__(self, clock, event_ref=None):
        """
        @param event_ref: The event that generated the DataPacket
        """
        super().__init__(clock=clock, event_ref=event_ref)


class ACKPacket(Packet):
    """
    An ACKPacket is created to reply to a generic packet.
    It uses null_event to be generated.
    """

    def __init__(self, source_drone, destination_drone, acked_packet, event_ref, clock):
        """
        @param simulator:
        @param source_drone:
        @param destination_drone:
        @param acked_packet:
        @param event_ref:
        """
        super().__init__(event_ref=event_ref, clock=clock)

        self.acked_packet = acked_packet
        self.source_drone = source_drone
        self.destination_drone = destination_drone


class HelloPacket(Packet):
    """
    The hello message is responsible to spread information about a particular UAV
    to the neighborhood
    """

    def __init__(self, source_drone, current_position, current_speed, next_target, event_ref, clock):
        """
        @param simulator:
        @param source_drone:
        @param current_position:
        @param current_speed:
        @param next_target:
        @param event_ref:
        """
        super().__init__(clock=clock, event_ref=event_ref)
        self.current_position = current_position
        self.speed = current_speed
        self.next_target = next_target
        self.source_drone = source_drone  # Don't use this