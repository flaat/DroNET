from dataclasses import dataclass

@dataclass
class Battery:
    """
    This class represents the battery used by the drone.
    """

    weight: float
    capacity: float