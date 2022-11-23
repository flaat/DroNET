
import src.utilities.utilities as util
from src.entities.uav_entities import DataPacket
from src.simulation.metrics import Metrics


class MediumDispatcher:

    def __init__(self, metric_class: Metrics):
        self.packets = []
        self.metric_class = metric_class

    def send_packet_to_medium(self, packet, src_drone, dst_drone, to_send_ts):
        """
        Simulates sending a packet from one drone to another with a specific timestamp, by inserting these values in
        a list.
        If the packet is a control packet, then increment the control packets counter by one.


        @param packet: the packet to be sent
        @param src_drone: the drone sending the packet
        @param dst_drone: the drone receiving the packet
        @param to_send_ts: current timestamp + delay
        @return: None
        """
        if isinstance(packet, DataPacket):
            #TODO: figure this out: the function is incomplete, it just skips (pass instruction). Can we delete it or do we want to implement this?

            #self.metric_class.all_data_packets_in_simulation += 1
            pass

        else:

            self.metric_class.all_control_packets_in_simulation += 1

        self.packets.append((packet, src_drone, dst_drone, to_send_ts))

    def run_medium(self, current_ts):
        """
        Delivers the messages found in the packets list to their respective destinations. The following checks are
        done before performing a delivery:
            - Current timestamp needs to be equal to the timestamp in the packet.
            - The drones need to be inside their communication range.
            - The packet must successfully traverse the medium channel (it has a small chance of being lost).

        @param current_ts: current timestamp
        @return: None
        """

        if self.subfunction1(current_ts) != self.subfunction2(current_ts):
            print("List 1 ", self.subfunction1(current_ts))
            print("List 2 ", self.subfunction2(current_ts))

        # If a message is delivered remove it from the list of packets to send.
        to_drop_indices = []
        original_self_packets = self.packets[:]
        self.packets = []

        for i in range(len(original_self_packets)):
            packet, src_drone, dst_drone, to_send_ts = original_self_packets[i]

            if to_send_ts == current_ts:  # time to send this packet
                to_drop_indices.append(i)

                if src_drone.identifier != dst_drone.identifier:
                    drones_distance = util.euclidean_distance(src_drone.coords, dst_drone.coords)
                    if drones_distance <= min(src_drone.communication_range, dst_drone.communication_range):
                        if dst_drone.routing_algorithm.channel_success(drones_distance):
                            dst_drone.routing_algorithm.drone_reception(src_drone, packet, current_ts)  # reception of a packet

        # TODO: unroll this and make it more readable.
        original_self_packets = [original_self_packets[i] for i in range(len(original_self_packets)) if i not in to_drop_indices]
        self.packets = original_self_packets + self.packets
