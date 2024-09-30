from algorithm import AlgorithmBase
from tqdm import tqdm
import random
class RandomSelect(AlgorithmBase):
    def __init__(self, RC, verbose=True):
        super().__init__()
        self._verbose = verbose
        self._RC = RC

    def run(self, network, k):
        assert k <= network.number_of_nodes(), "network节点个数小于k"
        S = []
        for _ in range(self._RC):
            S.append(list(random.sample(network.nodes(), k)))
    
        return S