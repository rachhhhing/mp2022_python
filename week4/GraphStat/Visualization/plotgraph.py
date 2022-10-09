import networkx as nx
import matplotlib.pyplot as plt

def plot_ego(graph,node_id):
    """
    绘制某节点的局部网络
    """
    ego = nx.Graph()
    #ego = nx.ego_graph(graph, node_id)
    
    #构建ego network
    for nei in graph[node_id]:          
        ego.add_edge(node_id, nei)          # 把该节点的所有边加进去
        for nei_nei in graph[nei]:
            if nei_nei in graph[node_id]:   # 把该节点邻居之间的边加进去
                ego.add_edge(nei, nei_nei)
    #绘图
    pos = nx.spring_layout(ego)             # 节点中心布局
    colors = range(len(ego[node_id])+1)
    nx.draw(ego, pos, with_labels=True, font_size = 6, node_color=colors, cmap=plt.cm.Reds_r, edge_color='gray', width=0.5)
    plt.show()

def plotdegree_distribution(graph):
    """
    绘制度的分布直方图
    """
    degree = []
    for key in graph:
        de = len(graph[key])
        degree.append(de)
    y, bins, patches = plt.hist(degree, bins=7, log=True, align='left')
    for i in range(len(y)):
        plt.text(bins[i], y[i]*1.02, int(y[i]), fontsize=12, horizontalalignment="center") # 打标签
    plt.title('degree distribution')    # 标题
    plt.xlabel('degree')                # x轴名
    plt.ylabel('frequency')             # y轴名
    #plt.savefig('度分布直方图' + '.png')
    plt.show()