import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "../")) 
from diffusionModel import MLIC, MLICWeighter
from algorithm import BasedDegree, RCC, PSOBMIM, CELF, RandomSelect, Greedy, FEC
from dataset import load_networks
from utils import load_json, save_json
from network import MLN
from constant import RESULT_PATH
import os
if __name__=="__main__":

    ## 定义多个多层网络
    networks = load_networks(["CKM", "Gallus", "CElegans", "Multi-Soc-wiki-Vote", "Multi_lastfm_asia", "arXiv-Netscience"], "undirected")

    ## 定义一个权重生成器
    weighter = MLICWeighter("fixed_random", inter_p=0.05, inter_range = (0, 0.1), intra_range=(0, 1), seed=0)
    
    ## 定义一个传播模型
    mlic = MLIC(weighter=weighter, MC=10000)
    

    ## 定义随机连通中心性算法
    rcc = RCC(1000, 10, 4, 0.5, False)
    rcc.set_name("rcc")
    
    ## 定义度中心性算法
    bd = BasedDegree()
    bd.set_name("degree")

    ## 定义离散粒子群算法
    psobmim = PSOBMIM(mlic, rcc, beta=0.3, num_particles = 100, max_iterations=140, c1=1.2, c2=1.2, is_NO=True)
    psobmim.set_name("PSOBMIM")

    ## 定义CELF算法
    celf = CELF(mlic)
    celf.set_name("CELF")

    ## 定义贪心算法
    greedy = Greedy(mlic)

    fec = FEC()
    ## 定义random算法
    # rs = RandomSelect()
    # rs.set_name("random")
    
    algs = [fec]

    result = {}
    for net in networks:
        result[net.get_name()] = {}
        for alg in algs:
            alg(net, 50)
            result[net.get_name()][alg.get_name()] = alg.running_time()


    print(result)
    # temp = load_json(os.path.join(RESULT_PATH, "running_time_result.json"))
    # # for key in result:
    # #     temp[key] = result[key]
    # # save_json(temp, os.path.join(RESULT_PATH, "running_time_result.json"))
    # for key in result:
    #     for key1 in result[key]:
    #         temp[key][key1] = result[key][key1]
    # save_json(result, os.path.join(RESULT_PATH, "running_time_result.json"))