import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "../")) 
from diffusionModel import MLIC, MLICWeighter
from algorithm import RCC, PSOBMIM
from dataset import load_networks
from evalution import Paramlator, ApproxFunc
from utils import save_json
from constant import RESULT_PATH
from network import MLN
import numpy as np

def trial(networks, alg, k):
    result = {}
    for network in networks:
        alg(network, k)
        result[network.get_name()] = np.array(alg.__history__()["global_best_fitness"])[list(range(1, 201, 1))].tolist()
    return result
if __name__=="__main__":

    ## 定义多个多层网络
    networks = load_networks(["CKM", "Gallus", "CElegans", "Multi-Soc-wiki-Vote", "Multi_lastfm_asia", "arXiv-Netscience"], "undirected")

    ## 定义一个权重生成器
    weighter = MLICWeighter("fixed_random", inter_p=0.05, inter_range = (0, 0.1), intra_range=(0, 1), seed=0)
    
    ## 定义一个传播模型
    mlic = MLIC(weighter=weighter, MC=1000)
    
    ## 定义衡量指标
    AF = ApproxFunc(mlic, False)
    AF.set_name("MLEDV")

    ## 定义随机连通中心性算法
    rcc = RCC(1000, 10, 4, 0.5, False)
    rcc.set_name("rcc")
    
    k = 50
    ## 定义算法bpsomim
    dpsobmim = PSOBMIM(mlic, rcc, beta=0.4, num_particles=100, max_iterations=201, w=0.8, c1=1.2, c2=1.2, is_NO=False)
    changed_attr = {
        "CKM":{"beta":0.4},
        "Gallus":{"beta":0.4},
        "CElegans":{"beta":0.4},
        "Multi-Soc-wiki-Vote":{"beta":0.3},
        "Multi_lastfm_asia":{"beta":0.2},
        "arXiv-Netscience":{"beta":0.2},
    }
    dpsobmim.set_changed_attr_by_network(changed_attr)
    result1 = trial(networks, dpsobmim, k)
    
    result = {"config":{"max iterations":list(range(1, 201, 1))}}
    result["result"] = result1
    print(result1)
    save_json(result, os.path.join(RESULT_PATH, "result_dpsomim_np_100_w_0__c1_2_c2_2_justify_ni.json"))