""" To clean. """

import pathlib
import matplotlib.pyplot as plt
import pandas as pd
import pickle
from src.simulation.configurator import Configurator
from src.utilities.formulas import *


# TODO: functions are never used, also they are VERY simple, why not implement them where we need them?
def pickle_data(data, filename):
    """ save the metrics on file """
    with open(filename, 'wb') as out:
        pickle.dump(data, out)


def unpickle_data(filename):
    """ load the metrics from a file """
    with open(filename, 'rb') as handle:
        obj = pickle.load(handle)
    return obj


def save_txt(text, file):
    with open(file, "w") as f:
        f.write(text)


class LimitedList:
    """ Time window """

    def __init__(self, threshold=None):
        self.llist = []
        self.threshold = threshold

    def append(self, el):
        if self.threshold and self.threshold < len(self.llist) + 1:
            self.llist = self.llist[1:]
        self.llist.append(el)

    def __len__(self):
        return len(self.llist)

    def __getitem__(self, index):
        return self.llist[index]


def make_path(fname):
    path = pathlib.Path(fname)
    path.parent.mkdir(parents=True, exist_ok=True)


def plot_X(X, plt_title, plt_path, window_size=30, is_avg=True):
    if len(X) >= window_size:
        df = pd.Series(X)
        scatter_print = X[window_size:]
        to_plot_data = df.rolling(window_size).mean()[window_size:]

        plt.clf()
        plt.plot(range(len(scatter_print)), to_plot_data, label="Moving Average-" + str(window_size))
        if is_avg:
            plt.plot(range(len(scatter_print)), [np.average(scatter_print)] * len(scatter_print), label="avg")

        plt.legend()
        plt.title(plt_title)
        plt.savefig(plt_path)
        plt.clf()


""" This class handles the return to depot for
    the drones, such that they return to the depot in a coordinated fashion
    currently is based on channel -> in future can also handle cluster head/waypoints
"""


class PathToDepot():

    def __init__(self, x_position):
        self.x_position = x_position
        self.config = Configurator().configuration

    def next_target(self, drone_pos):
        """ based on the drone position return the next target:
            |-> channel position or cluster head position
            |-> the depot if the drones are already in the channel or have overpass the cluster head
        """
        # only channel mode
        if abs(drone_pos[
                   0] - self.x_position) < 1:  # the drone is already on the channel with an error of 1 meter
            return self.config.depot_coordinates
        else:
            return self.x_position, drone_pos[1]  # the closest point to the channel


def measure_scaler(measure, dom_start, dom_target):
    """ Scales the measure value in the start domain [Type, min, max], in the target domain. """
    return (measure - dom_start[1]) / (dom_start[2] - dom_start[1]) * (dom_target[2] - dom_target[1]) + dom_target[1]
