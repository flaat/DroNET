from src.entities.packets.packets import DataPacket
from src.entities.simulated_entities import Entity


# class EventGenerator(SimulatedEntity):
#
#     def __init__(self, height, width, random_generator):
#         """ uniform event generator """
#         super().__init__(clock=None)
#         self.height = height
#         self.width = width
#         self.random_generator = random_generator
#
#     def uniform_event_generator(self):
#         """ generates an event in the map """
#         x = self.random_generator.randint(0, self.height)
#         y = self.random_generator.randint(0, self.width)
#         return x, y
#
#     def poisson_event_generator(self):
#         """ generates an event in the map """
#         pass


class Event(Entity):
    """
    An Event object is any kind of event that the drone detects in the Area-of-Interest
    """

    def __init__(self, coordinates: tuple, current_time: int, clock, deadline=None):
        """
        @param coordinates:
        @param current_time:
        @param simulator:
        @param deadline:
        """

        super().__init__(identifier=id(self), clock=clock)
        self.current_time = current_time

        # One can specify the deadline or just consider as deadline now + EVENTS_DURATION
        # The deadline of an event represents the estimate of the drone that the event will be no more
        # interesting to monitor.
        # TODO: comments say now + EVENTS_DURATION (which is something in the config file) but the value is hardcoded to "100". In config file value is set to "2000"
        self.deadline = current_time + 100

        # add metrics: all the events generated during the simulation
        # GENERATED_EVENTS
        # TODO: ????
        if not coordinates == (-1, -1) and not current_time == -1:
            pass

    @property
    def is_expired(self):
        """
        Check if the Event is expired
        @return: True if the event is expired False otherwise
        """
        return self.clock > self.deadline

    def as_packet(self, drone):
        """
        Build a Packet out of the Event, by default the packet has the same deadline of the event
        so the packet expire at the same time of the event.
        @param drone:
        @return:
        """

        # Notice: called only when a packet is created

        packet = DataPacket(clock=self.clock, event_ref=self)
        packet.add_hop(drone)

        return packet

    def __repr__(self):
        """
        @return:
        """

        return f"Event id:{str(self.identifier)} coordinates:{str(self.coordinates)}"

    def to_json(self):
        """
        @return:
        """

        event_dict = {
            "Event_identifier": self.identifier,
            "Event_coordinates": self.coordinates,
            "Event_generation_time": self.current_time,
            "Event_deadline": self.deadline
        }

        return event_dict
