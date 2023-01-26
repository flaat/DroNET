from abc import ABC, abstractmethod


class EnergyModel(ABC):
    """
    Base abstract class that represents all energy models
    """

    @abstractmethod
    def __tick(self, **data):
        """
        This method gets called every simulation time step. It will use energy models function to drain the battery.
        :param data: Dictionary containing all data for the energy consumption
        :return:
        """

    pass