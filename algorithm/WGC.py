"""Weighted Gravity Centrality
"""
from algorithm import AlgorithmBase
from network import MLN
import networkx as nx
class WGC(AlgorithmBase):
    def __init__(self, R, verbose=True):
        super().__init__()
        self._verbose = verbose
        self._R = R
    
    
    
    def run(self, network:MLN, k):   
        
        wgc = {} 
        nodes = network.nodes()
        self.shortest_paths = []
        for i in range(network.number_of_layers()):
            self.shortest_paths.append(dict(network.sjh))
            
        if(self._verbose):
            print(self.get_name()+"算法完成最短路径计算")    
        
        for i in range(network.number_of_nodes() - 1):
            for j in range(i+1, network.number_of_nodes()):
                    if(nodes[i] not in wgc):
                        wgc[nodes[i]] = 0
                    if(nodes[j] not in wgc):
                        wgc[nodes[j]] = 0
                   
                    sd = self.social_distance(network, nodes[i], nodes[j])
                   
                    if(sd != 0):
                        temp = len(network.neighbors(nodes[i])) * len(network.neighbors(nodes[j])) / (sd * sd)
                        wgc[nodes[i]] += temp
                        wgc[nodes[j]] += temp
        wgc = sorted(wgc.items(), key=lambda x:x[1], reverse=True)
        S = []
        
        for i in range(k):
            S.append(wgc[i][0])
            
        return S
        
    def social_distance(self, network:MLN, source=None, target=None):
        sd = 0
        for i in range(network.number_of_layers()):
            if(source not in self.shortest_paths[i]):
                shortest_paths = []
            elif(target not in self.shortest_paths[i][source]):
                shortest_paths = []
            else:
                shortest_paths = self.shortest_paths[i][source][target]

            max_shortest_path = 0
            
            for shortest_path in shortest_paths:  
                
                if(len(shortest_path) <= self._R):
                    temp = 1
                    for j in range(len(shortest_path) - 1):
                        temp *= network.layers[i][shortest_path[j]][shortest_path[j+1]]["weight"]
                    if(temp > max_shortest_path):
                        max_shortest_path = temp     
            sd += max_shortest_path
                
        if(sd == 0):
            return 0
        else:
            return 1 / sd