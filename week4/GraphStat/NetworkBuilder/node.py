import pandas as pd
import networkx as nx

def init_node(filename):
    """
    从数据文件中加载所有节点及其属性，返回dataframe结构

    :param filename:数据文件路径
    :return node:加载后的所有节点，dataframe结构
    """
    with open(filename,'r',encoding='utf-8') as f:
        data = pd.read_csv(f)
    return data

def get_degree(data,graph):
    """
    获取节点的度，存入data数据表

    :param data:储存节点的数据表
    :param graph:加载的图结构
    :return degree:返回某节点的度
    """
    degree = []
    for i in range(len(data)):
        de = len(graph[data.iloc[i,5]])     # graph第一层结构为以节点编号为key,其相邻节点为value
        degree.append(de)
    data['degree'] = degree
    return data

def print_node(data,node_id):
    """
    输出某节点的全部信息

    :param data:加载后的所有节点
    :param node_id:需要输出的某节点ID
    """
    print("-----ID为{}的节点信息-----".format(node_id))
    print(data.loc[node_id])