import src.utilities.utilities as util
from src.routing_algorithms.BASE_routing import BaseRouting


class RandomRouting(BaseRouting):

    def __init__(self, drone, simulator):
        BaseRouting.__init__(self, simulator=simulator, drone=drone)

    def relay_selection(self, opt_neighbors, packet):
        """
        This function returns a random relay for packets.

        @param opt_neighbors: a list of tuples (hello_packet, drone)
        @return: a random drone as relay
        """

        return self.simulator.rnd_routing.choice([v[1] for v in opt_neighbors])
