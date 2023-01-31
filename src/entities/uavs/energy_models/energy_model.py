from abc import ABC, abstractmethod


class EnergyModel(ABC):
    """
    Base abstract class that represents all energy models
    """

    '''
    FATTO:
    1) funzione richiamata ad ogni simulation tick: per metterci aggiornamento modello energetico
    2) refactorare vecchia funzione di movimento
    
    TODO:
    1) opzioni path in config enum invece che 3 booleani a caso e indipendenti.
    3) caricare dati tipo massa, velocita' etc da file. Piu file di config?
    4) come scegliere diversi modelli energetici
    '''

    @abstractmethod
    def tick(self, **data):
        """
        This method gets called every simulation time step. It will use energy models function to drain the battery.
        :param data: Dictionary containing all data for the energy consumption
        :return:
        """

    pass