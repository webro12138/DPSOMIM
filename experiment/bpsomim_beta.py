import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "../")) 
from diffusionModel import MLIC, MLICWeighter
from algorithm import RCC, PSOBMIM
from dataset import load_networks
from evalution import Paramlator, ApproxFunc
from utils import save_json
from constant import RESULT_PATH, EXP_DATASETS
from network import MLN
import numpy as np

if __name__=="__main__":

    ## 定义多个多层网络
    networks = load_networks(["CKM", "Gallus", "CElegans", "Multi-Soc-wiki-Vote", "Multi_lastfm_asia", "arXiv-Netscience"], "undirected")
    # networks = load_networks(["arXiv-Netscience"], "undirected")
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
    

    ## 定义算法bpsomim
    dpsobmim = PSOBMIM(mlic, rcc, beta=0.1, num_particles=100, max_iterations=100, w=0.8, c1=1.2, c2=1.2, is_NO=False)
    
    ## 定义参数调节器
    pl = Paramlator(AF, networks, 50, dpsobmim)
    
    result = pl(beta=list(np.arange(0.1, 1.01, 0.1)))
    print(result)
    save_json(result, os.path.join(RESULT_PATH, "result_dpsomim_ni_100_np_100_w_0__c1_2_c2_2_justify_beta.json"))