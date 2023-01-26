import json


class SimulationHistory:

    def __init__(self):
        self.history = {
            "energy": [],
            "communication": []
        }

    def write_event(self, event: str, category: str) -> None:
        """
        Write an event on the dictionary
        :param category:
        :param event:
        :return:
        """

        self.history[category].append(event)

    def to_json(self, path: str) -> None:
        """
        Save the history dict in path
        :param path: a string that specifies a path
        :return: None
        """

        with open(path+"Simulation_history.json", 'w') as outfile:

            json.dump(self.history, outfile)
