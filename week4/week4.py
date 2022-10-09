from GraphStat.NetworkBuilder import graph,node,stat
from GraphStat.Visualization import plotgraph,plotnodes

#G = graph.init_graph('large_twitch_edges.csv')
#data = node.init_node('large_twitch_features.csv')
#data_add_degree = node.get_degree(data,G)
#node.print_node(data_add_degree,0)

"""
nodes_num = stat.get_node_number(G)
edges_num = stat.get_edge_number(G)
average_dgree = stat.cal_average_dgree(G)
print("-----图的基本统计信息-----")
print(f"nodes number:{nodes_num}\nedges_num:{edges_num:.0f}\naverage degree:{average_dgree:.2f}")
"""
#print(stat.cal_degree_distribution(G))
#print(stat.cal_views_distribution(data))

#print("-----正在绘制节点的局部网络图-----")
#plotgraph.plot_ego(G, 0)
#print("-----正在绘制度的分布直方图-----")
#plotgraph.plotdegree_distribution(G)
#print("-----正在绘制节点views属性的分布直方图-----")
#plotnodes.plot_nodes_attr(data, 'views')