import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "../")) 
from diffusionModel import MLIC, MLICWeighter
from algorithm import RCC
from dataset import load_networks
from evalution import Paramlator, InfluenceSpread
from utils import save_json
from constant import RESULT_PATH, EXP_DATASETS
from network import MLN

if __name__=="__main__":

    ## 定义多个多层网络
    networks = load_networks(["CKM", "Gallus", "CElegans", "Multi-Soc-wiki-Vote", "Multi_lastfm_asia", "arXiv-Netscience"], "undirected")

    ## 定义一个权重生成器
    weighter = MLICWeighter("fixed_random", inter_p=0.05, inter_range = (0, 0.1), intra_range=(0, 1), seed=0)
    
    ## 定义一个传播模型
    mlic = MLIC(weighter=weighter, MC=10000)
    
    ## 定义衡量指标
    IS = InfluenceSpread(mlic, False)
    IS.set_name("influence spread")

    ## 定义随机连通中心性算法
    rcc = RCC(1000, 30, 4, 0.5, False)
    rcc.set_name("rcc")
    

    ## 定义参数调节器
    pl = Paramlator(IS, networks, 50, rcc)
    result = pl(_walk_length=list(range(10, 101, 10)))
    print(result)
    save_json(result, os.path.join(RESULT_PATH, "result_rcc_sn_1000_p_30_q_4_justify_wl.json"))
