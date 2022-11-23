
class SimulatedEntity:
    """ A simulated entity keeps track of the simulation object, where you can access all the parameters
    of the simulation. No class of this type is directly instantiable.
    """

    def __init__(self, simulator):
        self.simulator = simulator


# ------------------ Entities ----------------------
class Entity(SimulatedEntity):
    """ An entity in the environment, e.g. Drone, Event, Packet. It extends SimulatedEntity. """

    def __init__(self, identifier: int, coordinates: tuple, simulator):
        super().__init__(simulator)
        self.identifier = identifier  # the id of the entity
        self.coordinates = coordinates  # the coordinates of the entity on the map

    def __eq__(self, other):
        """ Entity objects are identified by their id. """
        if not isinstance(other, Entity):
            return False
        else:
            return other.identifier == self.identifier

    def __hash__(self):
        return hash((self.identifier, self.coordinates))
