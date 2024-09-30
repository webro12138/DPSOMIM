from algorithm import AlgorithmBase
from tqdm import tqdm
from utils import save_json, load_json
from copy import deepcopy
import networkx as nx
import numpy as np
import random
 
class SAIM(AlgorithmBase):
    def __init__(self, diffusion_model, cs_alg=None, beta=0.4, T_h=1800, T_f=20, theta=5, features_save_path=None, features_read_path=None, verbose=True):
        super().__init__()
        self._diffusion_model = diffusion_model
        self._diffusion_model.set_verbose(False)
        self._beta = beta
        self._features_save_path = features_save_path
        self._features_read_path = features_read_path
        self._T_h = T_h
        self._T_f= T_f
        self._theta = theta
        self._verbose = verbose
        self._cs_alg = cs_alg
    
    def set_setting(self, network, k):
        self.network = network
        self.k = k
        self.search_space = []
        
    def Noc(self):
        return int(self.k + (self.network.number_of_nodes() - self.k) * np.power(self._beta * self.k / self.network.number_of_nodes(), 1-self._beta))

    def run(self, network, k):
        self.set_setting(network, k)
        if(self._cs_alg != None):
            self.search_space = self._cs_alg(network, self.Noc())
     
        else:
            self.search_space = network.nodes()
            
        S = self.SA()
        
        return S

    def SA(self):
        r = 0
        if(self._cs_alg != None):
            S = self.search_space[0:self.k]
        else:
            S = random.sample(self.search_space, self.k)
        influence_spread = self._diffusion_model.approx_func(self.network, S)
        new_S = deepcopy(S)
        new_influence_spread = 0
        while(self._T_h > self._T_f):
            for _ in range(20):
                C = set(self.search_space) - set(S)
                s = random.choice(list(C))
                index = random.choice(list(range(len(S))))
                temp = new_S[index] 
                new_S[index] = s
                new_influence_spread = self._diffusion_model.approx_func(self.network, new_S)
                if(new_influence_spread > influence_spread):
                    S[index] = s
                    influence_spread = new_influence_spread
                    r = 0
                else:
                    new_S[index] = temp
                    r += 1   
            self._T_h = self._T_h - self._theta * np.log(r + 1)
            if(self._verbose):
                print(f"正在进行模拟退火|{self._T_h:.4f}|{self._T_f:.4f}|fitness:{influence_spread:.4f}        ", end="\r")
        if(self._verbose):
            print("                                                                           ",end="\r")    
        return S