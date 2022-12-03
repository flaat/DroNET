from src.simulation.configuration import Configuration
import json
class SingletonMeta(type):
    """
    The metaclass that allows us to spawn singleton classes.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Configurator(metaclass=SingletonMeta):
    configuration = None

    def load_default_config(self):
        """
        Loads the file default.json
        """
        self.load_config("config/default.json")

    def load_config(self, path: str):
        """
        Loads a generic .json configuration file located at "path"
        @param path: file path for the configuration
        @return:
        """

        config_file= open(path)
        json_parameters = json.load(config_file)

        simulation_parameters = json_parameters['simulation']
        drone_parameters = json_parameters['drone']
        depot_parameters = json_parameters['depot']
        event_parameters = json_parameters['event']
        routing_parameters = json_parameters['routing']

        self.configuration = Configuration(
            # Simulation
            simulation_parameters['simulationName'],
            simulation_parameters['timeStepDuration'],
            simulation_parameters['simulationLength'],
            simulation_parameters['seed'],
            simulation_parameters['numberOfDrones'],
            simulation_parameters['environmentWidth'],
            simulation_parameters['environmentHeight'],
            simulation_parameters['showPlot'],
            simulation_parameters['probSizeCell'],

            # Drones
            drone_parameters['droneCommunicationRange'],
            drone_parameters['droneSensingRange'],
            drone_parameters['droneSpeed'],
            drone_parameters['droneMaxBufferSize'],
            drone_parameters['droneMaxEnergy'],
            drone_parameters['droneRetransmissionDelta'],
            drone_parameters['droneCommunicationSuccess'],

            # Depot
            depot_parameters['depotCommunicationRange'],
            tuple(depot_parameters['depotCoordinates']),

            # Events
            event_parameters['eventDuration'],
            event_parameters['eventGenerationProbability'],
            event_parameters['eventGenerationDelay'],

            # Routing
            routing_parameters['packetMaxTimeToLive'],
            routing_parameters['routingAlgorithm'],
            routing_parameters['channelErrorType'],
        )