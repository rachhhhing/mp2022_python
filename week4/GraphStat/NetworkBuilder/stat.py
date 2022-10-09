import numpy as np
import pandas as pd

def get_node_number(graph):
    """
    计算节点数
    """
    nodes_num = len(graph)
    return nodes_num

def get_edge_number(graph):
    """
    计算边数
    """
    edges = 0
    for node in graph:
        edges += len(graph[node])
    edges_num = edges / 2
    return edges_num

def cal_average_dgree(graph):
    """
    计算网络中的平均度
    """
    nodes_num = len(graph)
    edges_num = 0
    for node in graph:
        edges_num += len(graph[node])
    return edges_num/nodes_num

def cal_degree_distribution(graph):
    """
    计算网络的度分布

    :return degree_dis:返回度分布，series类型
    """
    degree = []
    for key in graph:                       # 统计每个节点的度，存成列表
        de = len(graph[key])
        degree.append(de)
    degree_df = pd.DataFrame(degree)        # 将列表转化成dataframe储存
    degree_dis = degree_df.value_counts()   # 用dataframe的函数完成统计
    return degree_dis

def cal_views_distribution(data):
    """
    计算views属性的分布

    :return views_dis:返回views分布，series类型
    """
    views_dis = data['views'].value_counts()
    return views_dis