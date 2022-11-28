import src.utilities.utilities as util
from src.entities.packets.packets import HelloPacket, DataPacket
from src.entities.uavs.drone import Drone

#TODO: does this simulate (in an extremely simplistic way) the network stack?

"""
The MediumDispatcher simulates the network stack.
"""

class MediumDispatcher:

    def __init__(self, simulator):
        """

        @param simulator:
        """
        self.packets = []
        self.simulator = simulator

    def send_packet_to_medium(self, packet_to_send: HelloPacket, source_drone: Drone, destination_drone: Drone, to_send_ts: int):
        """
        Simulates sending a packet from one drone to another with a specific timestamp, by inserting these values in
        a list.
        If the packet is a control packet, then increment the control packets counter by one.

        @param packet_to_send: The Packet to send
        @param source_drone: Source Drone
        @param destination_drone: Destination Drone
        @param to_send_ts: time stamp to send the packet, equal to the timestamp of a drone plus some delay
        @return: None
        """

        if isinstance(packet_to_send, DataPacket):

            self.simulator.metrics.all_data_packets_in_simulation += 1

        else:

            self.simulator.metrics.all_control_packets_in_simulation += 1

        self.packets.append((packet_to_send, source_drone, destination_drone, to_send_ts))

    def run_medium(self, current_ts: int):
        """
        Delivers the messages found in the packets list to their respective destinations. The following checks are
        done before performing a delivery:
            - Current timestamp needs to be equal to the timestamp in the packet.
            - The drones need to be inside their communication range.
            - The packet must successfully traverse the medium channel (it has a small chance of being lost).

        @param current_ts: current timestamp
        @return: None
        """

        indices_to_drop = []
        self_packets_deep_copy = self.packets[:]

        self.packets = []

        for index, packet in enumerate(self_packets_deep_copy):

            packet_to_send, source_drone, destination_drone, to_send_ts = packet

            # time to send this packet_to_send
            if to_send_ts == current_ts:

                indices_to_drop.append(index)

                if source_drone.identifier != destination_drone.identifier:

                    drones_distance = util.euclidean_distance(source_drone.coordinates, destination_drone.coordinates)

                    if drones_distance <= min(source_drone.communication_range, destination_drone.communication_range):

                        if destination_drone.routing_algorithm.channel_success(drones_distance):

                            # destination drone receives packet_to_send
                            destination_drone.routing_algorithm.drone_reception(source_drone, packet_to_send)

                            self.simulator.logger.add_drones_packet(timestep=self.simulator.cur_step,
                                                                    packet=packet_to_send,
                                                                    source_drone=source_drone)


        self_packets_deep_copy = [self_packets_deep_copy[i] for i in range(len(self_packets_deep_copy)) if i not in indices_to_drop]

        self.packets += self_packets_deep_copy

