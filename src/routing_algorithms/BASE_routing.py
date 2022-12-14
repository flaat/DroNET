from src.entities.events.event import Event
from src.entities.packets.packets import Packet, HelloPacket, DataPacket, ACKPacket
from src.simulation.configurator import Configurator
import abc


class BaseRouting(metaclass=abc.ABCMeta):
    """
    This class is used as baseclass to build new routing protocols.
    """

    def __init__(self, drone, network_dispatcher):
        """
        @param drone: The drone that needs to perform routing
        """

        self.config = Configurator().configuration
        self.communication_error_type = None
        self.drone = drone
        self.current_n_transmission = 0
        self.hello_messages = {}  # { drone_id : most recent hello packet}
        self.network_dispatcher = network_dispatcher
        self.no_transmission = False

    @abc.abstractmethod
    def relay_selection(self, opt_neighbors: list, packet):
        """
        Abstract method to implement the routing protocol
        @param opt_neighbors: a list of neighbors drones
        """
        pass

    def routing_close(self):
        self.no_transmission = False

    def drone_reception(self, source_drone, packet: Packet):
        """
        This method handles the drones packet reception.
        @param source_drone: Drone that sent the packet
        @param packet: Packet sent
        @return:
        """

        if isinstance(packet, HelloPacket):

            source_drone_id = packet.source_drone.identifier

            self.hello_messages[source_drone_id] = packet  # add packet to our dictionary

        elif isinstance(packet, DataPacket):

            self.no_transmission = True
            self.drone.accept_packets([packet])

            null_event = Event(coordinates=(-1, -1),
                               current_time=-1,
                               clock=self.drone.clock)

            ack_packet = ACKPacket(source_drone=self.drone,
                                   destination_drone=source_drone,
                                   acked_packet=packet,
                                   event_ref=null_event,
                                   clock=self.drone.clock)

            self.unicast_message(packet_to_send=ack_packet,
                                 source_drone=self.drone,
                                 destination_drone=source_drone)

        elif isinstance(packet, ACKPacket):

            self.drone.remove_packets([packet.acked_packet])

            if self.drone.buffer_length == 0:
                self.current_n_transmission = 0
                self.drone.move_routing = False

    def drone_identification(self, drones: list):
        """
        It sends to the neighbours an HelloPacket
        @param drones: a list of Drones
        @return:
        """

        # still not time to communicate
        if self.drone.clock.current_time % self.config.hello_delay != 0:
            return 0

        null_event = Event(coordinates=(-1, -1),
                           current_time=-1,
                           clock=self.drone.clock)

        hello_packet = HelloPacket(source_drone=self.drone,
                                   current_position=self.drone.coordinates,
                                   current_speed=self.drone.speed,
                                   next_target=self.drone.next_target(),
                                   event_ref=null_event,
                                   clock=self.drone.clock)

        self.broadcast_message(packet_to_send=hello_packet,
                               source_drone=self.drone,
                               destination_drones=drones)

    def routing(self, drones: list):
        """
        @param drones:
        @return:
        """

        # set up this routing pass
        self.drone_identification(drones=drones)

        self.send_packets()

        # close this routing pass
        self.routing_close()

    def send_packets(self):
        """
        This function handles packets delivery to the depot or other drones.
        It has 3 flows:
            1) It is not possible to transmit packets or there are no packets to transmit
            2) The drone is close enough to the depot to offload the packets directly
            3) The drone have to find the best relay available following a policy
        @return:
        """

        # FLOW 1: if it is not possible to communicate with other Entities or there are no packets to send
        if self.no_transmission or self.drone.buffer_length == 0:
            return 0

        # FLOW 2: the Depot is close enough to offload packets directly
        if self.drone.distance_from_depot <= min(self.drone.communication_range,
                                                 self.drone.depot.communication_range):
            self.transfer_to_depot(depot=self.drone.depot)
            self.drone.move_routing = False
            self.current_n_transmission = 0
            return 0

        # FLOW 3: find the best relay through the routing algorithm
        else:

            opt_neighbors = []

            for hello_packet_id in self.hello_messages:

                hello_packet = self.hello_messages[hello_packet_id]

                # check if packet is too old, if so discard the packet
                if hello_packet.time_step_creation < self.drone.clock.current_time - self.config.old_hello_packet:
                    continue

                opt_neighbors.append((hello_packet, hello_packet.source_drone))

            if opt_neighbors:

                for packet in self.drone.all_packets:

                    best_neighbor = self.relay_selection(opt_neighbors=opt_neighbors, packet=packet)

                    if best_neighbor is not None:

                        # send packets
                        self.unicast_message(packet_to_send=packet,
                                             source_drone=self.drone,
                                             destination_drone=best_neighbor)
                    else:

                        continue

            self.current_n_transmission += 1

    def channel_success(self, drones_distance, no_error=False):
        """
        Precondition: two drones are close enough to communicate. Return true if the communication
        goes through, false otherwise.
        """

        assert drones_distance <= self.drone.communication_range

        return True

    def broadcast_message(self, packet_to_send: Packet, source_drone, destination_drones):
        """
        It Sends a message to all the neighbours
        @param packet_to_send:
        @param source_drone:
        @param destination_drones:
        @return:
        """

        for drone in destination_drones:
            self.unicast_message(packet_to_send=packet_to_send,
                                 source_drone=source_drone,
                                 destination_drone=drone)

    def unicast_message(self, packet_to_send: Packet, source_drone, destination_drone):
        """
        It Sends a message directly to a single drone
        @param packet_to_send:
        @param source_drone:
        @param destination_drone:
        @return:
        """

        self.network_dispatcher.send_packet_to_medium(packet_to_send=packet_to_send,
                                                      source_drone=source_drone,
                                                      destination_drone=destination_drone,
                                                      to_send_ts=source_drone.clock.current_time + self.config.lil_delta)

    def transfer_to_depot(self, depot):
        """
        self.drone is close enough to depot and offloads its buffer to it, restarting the monitoring
        mission from where it left it
        """
        depot.transfer_notified_packets(drone=self.drone)
        self.drone.empty_buffer()
        self.drone.move_routing = False
