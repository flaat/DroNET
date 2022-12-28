import numpy as np
from src.simulation.configurator import Configurator


class EventGenerator:

    def __init__(self):
        self.config = Configurator().configuration
        self.rnd_drones = np.random.RandomState(self.config.seed)
        self.rnd_event = np.random.RandomState(self.config.seed)

    def handle_events_generation(self, cur_step: int, drones: list):
        """
        at fixed time randomly select a drone from the list and sample on it a packet/event.

        :param cur_step: the current step of the simulation to decide whenever sample an event or not
        :param drones: the drones where to sample the event
        :return: nothing
        """
        if cur_step % self.config.event_generation_delay == 0:  # if it's time to generate a new packet
            # drone that will receive the packet:
            drone_index = self.rnd_drones.randint(0, len(drones))
            drone = drones[drone_index]
            drone.feel_event()
