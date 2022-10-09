import re
import os
import jieba
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from math import sin, asin, cos, radians, fabs, sqrt
from pyecharts.charts import Geo
from pyecharts import options as opts
from pyecharts.globals import GeoType

def cut_words(sen, stopwords_list):
    """
    分词函数：给出待分词语句，使用 jieba 分词，返回分词列表
    """
    wordlist = []
    for word in jieba.cut(sen, cut_all=False):
        if word not in stopwords_list:
            wordlist.append(word)
    return wordlist

def clean_text(filename):
    """
    清洗文件函数：清洗weibo评论数据，分词，将对应数据存成dataframe
    """
    emotion = ['anger.txt','disgust.txt','fear.txt','joy.txt','sadness.txt']
    path = ".\Anger makes fake news viral online-data&code\\data\\emotion_lexicon\\"
    for i in range(len(emotion)):               #将情绪词典加入jieba分词库
        jieba.load_userdict(os.path.normpath(path + emotion[i]))
    
    with open("D:\code\mp2022\week1\stopwords_list.txt", 'r', encoding='utf-8') as s:
        stopwords = s.read()
        stopwords_list = stopwords.split('\n')
    
    text_cut_list = []
    with open(filename,'r',encoding='utf-8') as f:
        print("----------正在清洗数据，请稍后----------")
        data = pd.read_csv(f, delimiter="\t")           # 读取文件存成df
        data.dropna()                                   # 补缺失值
        data.drop_duplicates(inplace=True)              # 去重复
        j = 1
        for i in range(len(data)):
            print('\r', j, "/ 00000", end = ''); j += 1 ##
            text = data.iloc[i,1]                       # 读取微博text
            #清洗微博
            text = re.sub(r"(回复)?(//)?\s*@\S*?\s*(:| |$)", " ", text)  # 去除正文中的@和回复/转发中的用户名
            #text = re.sub(r"\[\S+?]", "", text)         # 去除表情符号
            text = re.sub(r"#", "", text)               # 保留话题内容
            re.sub(r'http[:.]+\S+', '', text)           # 除去url
            text = re.sub(r"\s+", " ", text)            # 合并正文中过多的空格
            data.iloc[i,1] = text                       # 把清洗后的结果存进去
            text_cut = cut_words(text, stopwords_list)                  
            text_cut_list.append(text_cut)              # 将分词后的微博存成列表 
        data["text_cut"] = text_cut_list                # 把分词后的微博存进df
        print()
    return data

def emo_vector():
    """
    情绪分析函数：返回一个情绪向量，每一点的值对应该情绪词占的比例
    """
    print("----------正在分析情绪，请稍后----------")
    emodict = []
    path = ".\Anger makes fake news viral online-data&code\\data\\emotion_lexicon\\"
    filename = ['anger.txt','disgust.txt','fear.txt','joy.txt','sadness.txt']
    for i in range(len(filename)):                      # 加载情绪字典
        file = open(os.path.normpath(path + filename[i]),'r',encoding='utf-8')
        emodict.append([line.strip() for line in file.readlines()])
        file.close()
    
    def count(text_cut):                                # 记录每个情绪出现的次数
        emo_count = [0, 0, 0, 0, 0]
        for word in text_cut:
            if word in emodict[0]:
                emo_count[0] += 1
            if word in emodict[1]:
                emo_count[1] += 1
            if word in emodict[2]:
                emo_count[2] += 1
            if word in emodict[3]:
                emo_count[3] += 1
            if word in emodict[4]:
                emo_count[4] += 1
        emo_sum = sum(emo_count)
        if emo_sum == 0:                                # 无情绪时向量均为0
            emotion_vector = [0, 0, 0, 0, 0]
        else:
            emotion_vector = [i/sum(emo_count) for i in emo_count]  # 计算情绪向量
        return emotion_vector
    return count

def emo_kind():
    """
    情绪分析函数：返回一个情绪值，为情绪词数目最多的
    """
    print("----------正在分析情绪，请稍后----------")
    emodict = []
    path = ".\Anger makes fake news viral online-data&code\\data\\emotion_lexicon\\"
    filename = ['anger.txt','disgust.txt','fear.txt','joy.txt','sadness.txt']
    for i in range(len(filename)):                      # 加载情绪字典
        file = open(os.path.normpath(path + filename[i]),'r',encoding='utf-8')
        emodict.append([line.strip() for line in file.readlines()])
        file.close()

    def count(text_cut):                                # 记录每个情绪出现的次数
        emo_count = [0, 0, 0, 0, 0]
        for word in text_cut:
            if word in emodict[0]:
                emo_count[0] += 1
            if word in emodict[1]:
                emo_count[1] += 1
            if word in emodict[2]:
                emo_count[2] += 1
            if word in emodict[3]:
                emo_count[3] += 1
            if word in emodict[4]:
                emo_count[4] += 1
        emo_sum = sum(emo_count)
        emotion = ["anger", "disgust", "fear", "joy", "sadness"]
        if emo_sum == 0:                                # 无情绪时返回种类none
            emotion_kind = "none"
        else:
            emotion_kind = emotion[emo_count.index(max(emo_count))] # 找到最大值即对应的情绪
        return emotion_kind
    return count

def emo_time(weibo,emotion,time):
    """
    情绪的时间分析函数：提供想要分析的情绪种类及时间模式,返回该情绪的变化趋势并绘制图形

    weibo:微博数据，储存为dataframe格式
    emotion:想分析的情绪
    time:想分析的时间模式

    """
    print("----------正在进行时间分析，请稍后----------")
    #先建好时间的字典
    hour = ['{:0>2d}'.format(i) for i in range(24)]
    hour_dict = {}
    hour_dict = hour_dict.fromkeys(hour,0)

    week = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
    week_dict = {}
    week_dict = week_dict.fromkeys(week,0)

    month = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    month_dict = {}
    month_dict = month_dict.fromkeys(month,0)

    time_list = np.array(weibo["weibo_created_at"]).tolist()    # 取得每条微博创建时间
    emotion_list = np.array(weibo["text_emo"]).tolist()         # 取得每条微博的情绪
    if time == 'hour':
        count = [1 for i in range(24)]
        for tm in time_list:
            t = tm.split(' ')
            t = t[-3].split(':')
            count[hour.index(t[0])] += 1
            if emotion_list[time_list.index(tm)] == emotion:
                hour_dict[t[0]] += 1
        hour_value = []
        for hr in hour:
            hour_value.append(hour_dict[hr]/count[hour.index(hr)])
        plt.plot(hour,hour_value,'o-',color='r',label='hour_{}'.format(emotion))
        plt.xlabel("hour")                              # 横坐标名字
        plt.ylabel("percent")                           # 纵坐标名字
        plt.legend(loc = "best")                        # 图例
        for a,b in zip(hour,hour_value):
            plt.text(a,b+0.01,'%.2f' % (b),ha = 'center',va = 'bottom',fontsize=10)   # 标注点的数值
    elif time == 'week':
        count = [1 for i in range(7)]
        for tm in time_list:
            t = tm.split(' ')
            count[week.index(t[0])] += 1
            if emotion_list[time_list.index(tm)] == emotion:
                week_dict[t[0]] += 1
        week_value = []
        for wk in week:
            week_value.append(week_dict[wk]/count[week.index(wk)])
        plt.plot(week,week_value,'o-',color='b',label='week_{}'.format(emotion))
        plt.xlabel("week")                              # 横坐标名字
        plt.ylabel("percent")                           # 纵坐标名字
        plt.legend(loc = "best")                        # 图例
        for a,b in zip(week,week_value):
            plt.text(a,b+0.01,'%.2f' % (b),ha = 'center',va = 'bottom',fontsize=10)   # 标注点的数值
    elif time == 'month':
        count = [1 for i in range(12)]
        for tm in time_list:
            t = tm.split(' ')
            count[month.index(t[0])] += 1
            if emotion_list[time_list.index(tm)] == emotion:
                month_dict[t[1]] += 1
        month_value = []
        for mh in month:
            month_value.append(month_dict[mh]/count[month.index(mh)])
        plt.plot(month,month_value,'o-',color='y',label='month_{}'.format(emotion))
        plt.xlabel("month")                             # 横坐标名字
        plt.ylabel("percent")                           # 纵坐标名字
        plt.legend(loc = "best")                        # 图例
        for a,b in zip(month,month_value):
            plt.text(a,b+0.01,'%.2f' % (b),ha = 'center',va = 'bottom',fontsize=10)   # 标注点的数值
    else:
        print('Error!')
    #plt.savefig('{}_{}.png'.format(time,emotion),dpi=800)
    plt.show()

def get_distance(coord1, coord2):
    '''
    计算实际距离函数：将经纬度转化为公里数
    '''
    def hav(theta):
        s = sin(theta / 2)
        return s * s
    
    lat1 = radians(coord1[0])
    lng1 = radians(coord1[1])
    lat2 = radians(coord2[0])
    lng2 = radians(coord2[1])
    dlng = fabs(lng1 - lng2)
    dlat = fabs(lat1 - lat2)
    h = hav(dlat) + cos(lat1) * cos(lat2) * hav(dlng)
    distance = 2 * 6371 * asin(sqrt(h))
    return distance

def str_to_float(weibo_str):
    all_loc = []
    for item in weibo_str:
        loc = []
        x,y = map(str,item.split())
        x=x[1:];x=x[:-1];y=y[:-1]
        loc.append(float(x))
        loc.append(float(y))
        all_loc.append(loc)
    return all_loc

def emo_area(weibo, emotion, city, max_dis):
    '''
    情绪空间分析函数：根据指定的情绪分析其空间的分布情况

    weibo:微博数据，储存为dataframe格式
    emotion：分析的情绪
    city：以该城市为中心
    max_dis：为计入的最远距离

    '''
    locations = str_to_float(np.array(weibo["location"]).tolist())    # 取得每条微博创建时间
    emotions = np.array(weibo["text_emo"]).tolist()             # 取得每条微博的情绪

    city_coord = {
    'beijing'  : [39.92, 116.46],
    'shanghai' : [31.22, 121.48],
    'guangzhou': [23.16, 113.23],
    'chengdu'  : [30.67, 104.06]}
    center = city_coord[city]                                   # 获取中心城市的坐标

    dist_list = []
    for i in range(len(emotions)):
        # 只统计中心周围经纬度小于1范围内的情绪
        if (abs(locations[i][0] - center[0]) < 1) and (abs(locations[i][1] - center[1]) < 1):
            dist = get_distance(center, locations[i])
            dist_list.append([dist,emotions[i]])
    dist_list = sorted(dist_list, key = (lambda x:x[0]))        # 按与中心的距离排序
    
    count = 1;cnt = 0
    percent = []
    x = list(np.arange(0, max_dis, 0.1))                        # 按差0.1公里分段统计
    for i in x:
        while dist_list[count][0] < i:
            if dist_list[count][1] == emotion:
                cnt += 1
            count += 1
        percent.append(cnt/count)
    plt.plot(x,percent,label='{}_{}'.format(city,emotion))
    plt.xlabel("distance")                          # 横坐标名字
    plt.ylabel("percent")                           # 纵坐标名字
    plt.legend(loc = "best")                        # 图例
    #plt.savefig('{}_{}.png'.format(city,emotion),dpi=800)
    plt.show()

def text_geo(weibo):
    """
    情绪空间分布可视化：在某城市的地图上标出情绪点
    """
    address_list = str_to_float(np.array(weibo["location"]).tolist())
    emotion_list = np.array(weibo["text_emo"]).tolist()
    emo = {'sadness':5,'joy':15,'fear':25,'disgust':35,'anger':45}

    g = Geo()
    data_pair = []
    g.add_schema(maptype='北京')
    for k in range(len(emotion_list)):
        if emotion_list[k] != "none":
            data_pair.append((emotion_list[k]+str(k),emo[emotion_list[k]]))  
            g.add_coordinate(emotion_list[k]+str(k),address_list[k][1],address_list[k][0])
            # 定义坐标对应的名称，添加到坐标库中 add_coordinate(name, lng, lat)
    # 将数据添加到地图上
    g.add('', data_pair, type_=GeoType.EFFECT_SCATTER, symbol_size=5)
    # 设置样式
    g.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    # 自定义分段 color 可以用取色器取色
    pieces = [
        {'min': 1, 'max': 10, 'label': 'sadness', 'color': '#3700A4'},
        {'min': 10, 'max': 20, 'label': 'joy', 'color': '#81AE9F'},
        {'min': 20, 'max': 30, 'label': 'fear', 'color': '#E2C568'},
        {'min': 30, 'max': 40, 'label': 'disgust', 'color': '#FCF84D'},
        {'min': 40, 'max': 50, 'label': 'anger', 'color': '#DD0200'}
    ]
    # is_piecewise 是否自定义分段，变为true才能生效
    g.set_global_opts(
        visualmap_opts=opts.VisualMapOpts(is_piecewise=True, pieces=pieces),
        title_opts=opts.TitleOpts(title="北京-情绪分布"),)
    return g

def main():
    weibo = clean_text("weibo.txt")     #清洗数据
    emo_analyse = emo_kind()            #分析情绪
    #emo_analyse = emo_vector()
    text_emo = []
    for text_cut in weibo["text_cut"]:
        text_emo.append(emo_analyse(text_cut))
    weibo["text_emo"] = text_emo

    #emo_time(weibo,"joy","hour")        #分析joy情绪的小时变化规律
    #emo_time(weibo,"sadness","week")    #分析sadness情绪的周变化规律
    #emo_area(weibo, "joy", "beijing", 15)   #分析以北京为中点的joy情绪分布规律

    g = text_geo(weibo)   
    g.render('text_render.html')   # 渲染成html, 可用浏览器直接打开
    
if __name__ == '__main__':
    main()