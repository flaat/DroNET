"""
This model is based on:
R. D'Andrea,
"Guest Editorial Can Drones Deliver?,"
in IEEE Transactions on Automation Science and Engineering,
vol. 11, no. 3, pp. 647-648, July 2014, doi: 10.1109/TASE.2014.2326952.

"""

from src.entities.uavs.energy_models.energy_model import EnergyModel


class dandrea_energy_model(EnergyModel):
    """
    This class specifies a simplistic energy model
    """
    def __tick(self, **data):
        # TODO: Finish specifying variables in data (i'm looking at you Frank)
        """
        Function gets called every simulation time step
        :param data:
        :return:
        """

