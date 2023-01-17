from src.simulation.simulator import Simulator
from src.tests import *

def main():
    """ the place where to run simulations and experiments. """
    #test()
    simulate()


def simulate():
    sim = Simulator()   # empty constructor means that all the parameters of the simulation are taken from src.utilities.config.py
    sim.run()           # run the simulation
    sim.close()
def test():
    # path manager tests
    path_manager_tests()

if __name__ == "__main__":
    main()