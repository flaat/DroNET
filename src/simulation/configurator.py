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
            instance.load_default_config()
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

        config_file = open(path)
        json_parameters = json.load(config_file)

        path_drones = json_parameters['path drones']
        drawing = json_parameters['drawing']
        simulation_parameters = json_parameters['simulation']
        drone_parameters = json_parameters['drone']
        depot_parameters = json_parameters['depot']
        event_parameters = json_parameters['event']
        routing_parameters = json_parameters['routing']

        from src.routing_algorithms.random_routing import RandomRouting
        from src.routing_algorithms.q_learning_routing import QLearningRouting

        routing_algorithm = RandomRouting if routing_parameters['routingAlgorithm'] == "RND" else QLearningRouting

        self.configuration = Configuration(
            # Path Drones
            path_drones['circlePath'],
            path_drones['demoPath'],
            path_drones['pathFromJSON'],
            path_drones['JSONPathPrefix'],
            path_drones['randomSteps'],
            path_drones['randomStartPoint'],

            # Drawing
            drawing['plotSimulation'],
            drawing['waitSimulationStep'],
            drawing['skipSimulationStep'],
            drawing['drawSize'],
            drawing['showDirectionVector'],

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
            simulation_parameters['debug'],
            simulation_parameters['experimentsDir'],
            simulation_parameters['savePlot'],
            simulation_parameters['savePlotDir'],
            simulation_parameters['cellProbSizeR'],
            simulation_parameters['enableProbabilities'],

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
            routing_algorithm,
            routing_parameters['channelErrorType'],
            routing_parameters['communicationSuccessProbability'],
            routing_parameters['gaussianScale'],
            routing_parameters['packetMaxTimeToLive'],
            routing_parameters['retransmissionDelay'],
            routing_parameters['helloDelay'],
            routing_parameters['receptionGranted'],
            routing_parameters['lilDelta'],
            routing_parameters['oldHelloPacket'],
            routing_parameters['rootEvaluationData'],
            routing_parameters['nnModelPath'],
        )