"""
This model is based on:
R. D'Andrea,
"Guest Editorial Can Drones Deliver?,"
in IEEE Transactions on Automation Science and Engineering,
vol. 11, no. 3, pp. 647-648, July 2014, doi: 10.1109/TASE.2014.2326952.

"""

from src.entities.uavs.energy_models.energy_model import EnergyModel


class DandreaEnergyModel(EnergyModel):
    """
    This class specifies a simplistic energy model
    """

    def __init__(self, payload_mass, drone_mass, lift_to_drag_ratio, power_transfer_efficiency,
                 power_consumption_electronics, battery_capacity):
        # TODO: Definitely add units.
        # Only thing that's missing is speed, which we already have in the drone class.

        self.payload_mass = payload_mass
        self.drone_mass = drone_mass
        self.lift_to_drag_ratio = lift_to_drag_ratio
        self.power_transfer_efficiency = power_transfer_efficiency
        self.power_consumption_electronics = power_consumption_electronics

        self.battery_capacity = battery_capacity

    def tick(self, **data):
        """
        Function gets called every simulation time step
        :param data:
        :return:
        """

        self.battery_capacity -= (((self.payload_mass + self.drone_mass) * data["drone_speed"])
                                  / (
                                              370 * self.lift_to_drag_ratio * self.power_transfer_efficiency)) + self.power_consumption_electronics
