import src.utilities.utilities as util
from src.routing_algorithms.BASE_routing import BaseRouting
import random


class RandomRouting(BaseRouting):

    def __init__(self, drone, network_dispatcher):
        BaseRouting.__init__(self, drone=drone, network_dispatcher=network_dispatcher)

    def relay_selection(self, opt_neighbors, packet):
        """
        This function returns a random relay for packets.

        @param opt_neighbors: a list of tuples (hello_packet, drone)
        @return: a random drone as relay
        """

        return random.choice([v[1] for v in opt_neighbors])
