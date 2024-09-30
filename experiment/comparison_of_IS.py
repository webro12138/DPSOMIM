import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../")) 
from diffusionModel import MLIC, MLICWeighter
from algorithm import BasedDegree, RCC, PSOBMIM, CELF, RandomSelect, Greedy, WGC
from dataset import load_networks
from evalution import Evalution , InfluenceSpread
from utils import load_json, save_json
from network import MLN
from constant import RESULT_PATH
import os
if __name__=="__main__":

    ## 定义多个多层网络
    networks = load_networks(["CKM", "Gallus", "CElegans", "Multi-Soc-wiki-Vote", "Multi_lastfm_asia", "arXiv-Netscience"], "undirected")
    # networks = load_networks(["arXiv-Netscience"], "undirected")
    
    ## 定义一个权重生成器
    weighter = MLICWeighter("fixed_random", inter_p=0.05, inter_range = (0, 0.1), intra_range=(0, 1), seed=0)
    
    for network in networks:
        weighter.assign_weights(network=network)

    ## 定义一个传播模型
    MC = 10000
    mlic = MLIC(weighter=weighter, MC=MC)
    
    ## 定义衡量指标
    IS = InfluenceSpread(mlic, False)
    IS.set_name("影响力扩展度")

    ## 定义随机连通中心性算法
    rcc = RCC(1000, 10, 4, 0.5, False)
    rcc.set_name("rcc")
    
    ## 定义度中心性算法
    bd = BasedDegree()
    bd.set_name("degree")
    
    wgc = WGC(2)
    ## 定义离散粒子群算法
    psobmim = PSOBMIM(mlic, rcc, beta=0.4, num_particles=60, max_iterations=100, w=0.6, c1=1.2, c2=1.2, is_NO=True)
    psobmim.set_name("PSOBMIM")
    changed_attr = {
        "CKM":{"beta":0.4},
        "Gallus":{"beta":0.4},
        "CElegans":{"beta":0.4},
        "Multi-Soc-wiki-Vote":{"beta":0.3},
        "Multi_lastfm_asia":{"beta":0.2},
        "arXiv-Netscience":{"beta":0.2},
    }
    psobmim.set_changed_attr_by_network(changed_attr)  

    ## 定义CELF算法
    celf = CELF(mlic)
    celf.set_name("CELF")


    ## 定义贪心算法
    greedy = Greedy(mlic)

    ## 定义random算法
    rs = RandomSelect(RC=MC)
    rs.set_name("random")
 

    ## 定义评估器
    ev = Evalution([IS], networks, [wgc], list(range(5, 51, 5)))
    
    ## 开始评估
    result = ev(retain_alg=[psobmim.get_name(), rs.get_name()])
    # 保存评估结果

    print(result)
    save_json(result, os.path.join(RESULT_PATH, "fixed_result_wgc.json"))