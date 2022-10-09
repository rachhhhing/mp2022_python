import numpy as np
import matplotlib.pyplot as plt

def plot_nodes_attr(data, attr):
    """
    绘制图中节点属性的统计结果
    """
    attr_list = np.array(data[attr]).tolist()
    y, bins, patches = plt.hist(attr_list, bins=10, log=True, align='left')
    for i in range(len(y)):
        plt.text(bins[i], y[i]*1.02, int(y[i]), fontsize=12, horizontalalignment="center") # 打标签
    plt.title(attr + ' distribution')   # 标题
    plt.xlabel(attr)                    # x轴名
    plt.ylabel('frequency')             # y轴名
    #plt.savefig('attr'+'分布直方图' + '.png')
    plt.show()