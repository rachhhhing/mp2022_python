import pickle
import pandas as pd
import networkx as nx

def init_graph(filename):
    """
    从数据文件中加载所有边，构建图结构

    :param filename:数据文件路径
    :return graph:加载后的图结构
    """
    with open(filename,'r',encoding='utf-8') as f:
        data = pd.read_csv(f)
    edges = data.apply(lambda x: tuple(x), axis=1).values.tolist()

    #构建图结构
    G = nx.Graph()
    G.add_edges_from(edges)
    
    return G

def save_graph(graph):
    """
    序列化图信息，实现存储
    """
    with open('graph.pkl','wb') as f:
        pickle.dump(graph, f)

def load_graph(path):
    """
    反序列化图信息，实现加载
    """
    with open(path,'rb') as f:
        graph = pickle.loads(f)
    return graph