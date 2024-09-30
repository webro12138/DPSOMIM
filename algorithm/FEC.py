from algorithm import AlgorithmBase
import numpy as np
import networkx as nx
class FEC(AlgorithmBase):
    def __init__(self, alpha=2, beta=1.4, tol=1e-5, verbose=True):
        super().__init__()
        self._alpha = alpha
        self._beta = beta
        self._verbose = verbose
        self._tol=tol
        
    def run(self, network, k):
        """
        计算多层网络中每个节点的中心性得分，并选择中心性最高的 k 个节点。

        Args:
            network: 多层网络.
            k (int): 选择中心性最高的 k 个节点。

        Returns:
            list: 包含中心性最高的 k 个节点的列表。
        """
        # 创建一个矩阵 A，用于存储所有网络的邻接矩阵
        A = np.zeros((len(network.layers[0].nodes), len(network.layers[0].nodes), len(network.layers)))
        
        # 遍历每个网络，将邻接矩阵添加到 A 中

        nodes = network.nodes()
        for i, G in enumerate(network.layers):
            A[:,:,i] = nx.adjacency_matrix(G, nodelist=nodes, weight="weight").toarray()
    
        # 初始化节点中心性得分向量 x0
        x0 = np.ones(A.shape[0]) / np.sqrt(A.shape[0])
 
        # 使用 power_t2 函数计算中心性得分
        x, y, it = self.power_T2(A, x0, self._alpha, self._beta,tol=self._tol)
    
        # 选择中心性最高的 k 个节点
      
        sorted_indices = np.argsort(-x)
    
        
       
        top_k_nodes = [nodes[index] for index in sorted_indices[:k]]

        return top_k_nodes



    def power_T2(self, A, x0, a, b, tol):
        # 初始化x和y
        x = x0 / np.linalg.norm(x0, 1)
        y = np.einsum('ijt,i->jt', A, x)
        y = np.einsum("jt,j->t", y, x)  
        y = y/np.linalg.norm(y, 1)
    
        rex = 1
        rey = 1
        it = 0
        bool = False

        while rex > tol or rey > tol:
            xold = x
            yold = y

            # 计算新的x
            xx = np.einsum("ijt,j->it", A, x)
            xx = np.einsum("it,t->i",xx, y)
            xx = np.power(xx, 1/b)
            x = np.abs(xx) / np.linalg.norm(np.abs(xx), 1)

            # 计算新的y
        
            yy = np.einsum("ijt,i->jt", A, x)
            yy = np.einsum("jt,j->t", yy, x)
            yy = np.power(yy, 1/a)
            y = np.abs(yy) / np.linalg.norm(np.abs(yy), 1)

            # 计算相对误差
            rex = np.linalg.norm(xold - x) / np.linalg.norm(x)
            rey = np.linalg.norm(yold - y) / np.linalg.norm(y)

            # 输出收敛信息
            if rex <= tol and not bool:
                bool = True
                if(self._verbose):
                    print(f'>>{self.get_name()}中节点中心性向量在第 ({it + 1} 轮收敛)')
            if rey <= tol and not bool:
                bool = True
                if(self._verbose):
                    print(f'>>{self.get_name()}中节点中心性向量在第 ({it + 1} 轮收敛)')

            it += 1

        return x, y, it
