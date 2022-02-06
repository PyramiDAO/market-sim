
import multiprocessing as mp

class Treasury:

    def __init__(self, balance):
        # TODO add Vault/Strategy class 
        self.balance = balance
        # initialize a multipleprocessing Queue to hold the simulated results across different processors
        self.simulation_result_queue = mp.Queue()

    def get_simulation_result_queue(self):
        return self.simulation_result_queue