import csv
import time
import json
import jieba
import collections
from pylab import *
import pandas as pd
import matplotlib.pyplot as plt
from multiprocessing import Process, Queue
from matplotlib.font_manager import FontProperties  

def Map(q, content):
    '''
    Map进程读取文档路径并进行词频统计，返回该文本的词频统计结果。
    '''
    with open('week2/stopwords_list.txt', 'r', encoding='utf-8') as s:
        stopwords = s.read()
        stopwords_list = stopwords.split('\n')
    
    word_list = []
    word_count = {}
    for con in content:
        seg_list = jieba.cut(con, cut_all=False)        # 分词
        word_list.extend(seg_list)
    for word in word_list:                              # 过滤停用词并且统计词频
        if word not in stopwords_list:
            count = word_count.get(word, 0)
            word_count[word] = count + 1
    q.put(word_count)                                   # 将词频统计结果放进队列

def Reduce(q, save_path = 'week11/word_count.txt'):
    '''
    Reduce进程收集所有Map进程提供的文档词频统计，更新总的文档库词频，并在所有map完成后保存总的词频到文件。
    '''
    total_count = {}
    while True:
        word_count = q.get()
        if word_count is None:                          # 所有map结束后将总的词频写入文件
            count_sorted = collections.OrderedDict(sorted(total_count.items(), key=lambda dc:dc[1],reverse=True))
            with open('week11/total_word_count.txt', 'w', encoding='utf-8') as f:
                json_str = json.dumps(count_sorted, indent=0, ensure_ascii=False)
                f.write(json_str)
                f.write('\n')
            break
        else:
            for word in word_count:                     # 合并词频
                if word not in total_count:
                    total_count[word] = word_count[word]
                else:
                    total_count[word] += word_count[word]

def json_to_list(path):
    '''
    将json文件的content全部写入list中
    '''
    content_list = []
    with open(path, "r" ,encoding = "utf-8") as f:
        data = json.load(f)[:10000]                     # 读取每一条json数据
        for news in data:
            content_list.append(news['content'])
    print("共有 %d 条正文" % len(content_list))
    return content_list

if __name__=='__main__':
    content_list = json_to_list('week11/sohu_data.json')
    q = Queue()
    r = Process(target=Reduce, args=(q,))

    N = 50
    maps = []
    num = int(len(content_list)/N)
    for i in range(0,N):
        content = content_list[i*num:(i+1)*num]         # 根据Map进程数目分发文档
        m = Process(target=Map, args=(q, content))
        maps.append(m)
    
    start_time = time.time()
    for m in maps:                                      # 启动Map进程
        m.start()
    r.start()                                           # 启动Reduce进程
    for m in maps:
        m.join()
    q.put(None)                                         # 主进程发信号结束
    end_time = time.time()
    print('-----所有任务结束-----')
    
    with open('week11/time_count.csv','a',encoding='utf-8', newline="") as csvfile:
        f = csv.writer(csvfile)
        f.writerow([N, end_time-start_time])
    
    '''
    with open('week11/time.csv','r',encoding='utf-8') as f:
        df = pd.read_csv(f)
    plt.plot(df['N'], df['time'], color='#6495ED', linewidth=2.0)
    mpl.rcParams['font.sans-serif'] = ['SimHei']
    plt.xlabel("Map进程数目")
    plt.ylabel("运行时间")                 
    plt.title('运行时间-进程数目')
    plt.show()
    '''