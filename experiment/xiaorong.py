import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "../")) 
from diffusionModel import MLIC, MLICWeighter
from algorithm import BasedDegree, RCC, PSOBMIM, CELF, RandomSelect, Greedy
from dataset import load_networks
from evalution import Evalution , InfluenceSpread
from utils import load_json, save_json
from network import MLN
from constant import RESULT_PATH

if __name__=="__main__":

    ## 定义多个多层网络
    networks = load_networks(["CKM", "Gallus", "CElegans", "Multi-Soc-wiki-Vote", "Multi_lastfm_asia", "arXiv-Netscience"], "undirected")

    ## 定义一个权重生成器
    weighter = MLICWeighter("fixed_random", inter_p=0.05, inter_range = (0, 0.1), intra_range=(0, 1), seed=0)
    
    ## 定义一个传播模型
    mlic = MLIC(weighter=weighter, MC=10000)
    
    ## 定义衡量指标
    IS = InfluenceSpread(mlic, False)
    IS.set_name("影响力扩展度")

    ## 定义随机连通中心性算法
    rcc = RCC(1000, 30, 4, 0.5, False)
    rcc.set_name("rcc")

    max_iters = 100
    beta = 0.4
    w=0.6
    c1 = 1.2
    c2 = 1.2
    changed_attr = {
        "CKM":{"beta":0.4},
        "Gallus":{"beta":0.4},
        "CElegans":{"beta":0.4},
        "Multi-Soc-wiki-Vote":{"beta":0.3},
        "Multi_lastfm_asia":{"beta":0.2},
        "arXiv-Netscience":{"beta":0.2},
    }
    num_particles=50
    ## 定义DPSO
    dpso = PSOBMIM(mlic, num_particles = num_particles, beta=beta, max_iterations=max_iters, w=w, c1=c1, c2=c2, is_NO=False)
    dpso.set_name("DPSO")
    dpso.set_changed_attr_by_network(changed_attr)
    ## 定义DPSO + NO 
    
    dpso_no = PSOBMIM(mlic, num_particles = num_particles, beta=beta, max_iterations=max_iters, w=w, c1=c1, c2=c2, is_NO=True)
    dpso_no.set_name("DSPO_NO")
    dpso_no.set_changed_attr_by_network(changed_attr)
    ## 定义RCC + DPSO
    rcc_dpso = PSOBMIM(mlic, rcc,  num_particles = num_particles, beta=beta, max_iterations=max_iters, w=w, c1=c1, c2=c2, is_NO=False)
    rcc_dpso.set_name("RCC_DPSO")
    rcc_dpso.set_changed_attr_by_network(changed_attr)

    ## 定义RCC + PSOBMIM + NO
    psobmim = PSOBMIM(mlic, rcc, num_particles = num_particles, beta=beta, max_iterations=max_iters, w=w, c1=c1, c2=c2, is_NO=True)
    psobmim.set_name("PSOBMIM")
    psobmim.set_changed_attr_by_network(changed_attr)

    algs = [psobmim, rcc_dpso, dpso_no, dpso]
    k = 50

    result = {}
    for network in networks:
   
        print(">>开始在" + network.get_name()+"上做实验")
        result[network.get_name()] = []
        
        for alg in algs:
            alg(network, k)
            result[network.get_name()].append(alg.__history__())
    
    print(result)
    save_json(result, "xiaorong.json")
