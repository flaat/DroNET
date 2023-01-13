from src.simulation.simulator import Simulator


def main():
    """ the place where to run simulations and experiments. """
    simulate()


def simulate():
    sim = Simulator()   # empty constructor means that all the parameters of the simulation are taken from src.utilities.config.py
    sim.run()           # run the simulation
    sim.close()
def test():
    sim = Simulator()
    print(sim.config)

if __name__ == "__main__":
    main()