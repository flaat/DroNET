# from src.entities.depot.depots import Depot
# from src.entities.events.event import EventGenerator
# from src.entities.simulated_entities import  SimulatedEntity
# from src.simulation.configurator import Configurator
# import numpy as np
#
# class Environment(SimulatedEntity):
#     """ The environment is an entity that represents the area of interest on which events are generated.
#      WARNING this corresponds to an old view we had, according to which the events are generated on the map at
#      random and then maybe felt from the drones. Now events are generated on the drones that they feel with
#      a certain probability."""
#
#     def __init__(self, width, height):
#         super().__init__(clock=None)
#
#         self.config = Configurator().configuration
#         self.depot = None
#         self.drones = None
#         self.width = width
#         self.height = height
#         self.rnd_env = np.random.RandomState(self.config.seed)
#         self.event_generator = EventGenerator(height, width, self.rnd_env)
#         self.active_events = []
#
#     def add_drones(self, drones: list):
#         """ add a list of drones in the env """
#         self.drones = drones
#
#     def add_depot(self, depot: Depot):
#         """ add depot in the env """
#         self.depot = depot