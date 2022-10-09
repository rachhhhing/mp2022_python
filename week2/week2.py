import jieba                                            #用于分词
import collections                                      #用于词频统计
import math                                             #用于数学计算
import random                                           #用于生成随机数
import numpy as np                                      #用于数据处理
import pandas as pd                                     #用于数据处理
import matplotlib.pyplot as plt                         #用于绘图
from PIL import Image                                   #用于词云图获取图片
from wordcloud import WordCloud, ImageColorGenerator    #用于绘制词云图
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence         #用于深度学习词向量表征

def read_document(filename):
    """
    读取文档函数：按行划分，转成列表返回
    """
    with open(filename, 'r', encoding='utf-8') as f:
        data = pd.read_csv(f)       
        col_1 = data["content"]                         #获取第一列数据
        document_array = np.array(col_1)                
        document_list = document_array.tolist()         #转成列表
    return document_list

def cut_word(lis, stopwords_filename):
    """
    分词函数：使用jieba分词，过滤停用词，返回列表
    """
    jieba.load_userdict(stopwords_filename)             #添加停用词进自定义字典
    
    print("----------进行分词中，请稍等----------")
    wordlist = []
    for sen in lis:
        seg_list = jieba.cut(sen, cut_all=False)        #分词
        wordlist.extend(seg_list)
    return wordlist

def word_analyse(wordlist, stopwords_filename, n):
    """
    词频分析函数：统计wordlist中特定数目的高频词和低频词，过滤低频词，形成特征词集
    """
    with open(stopwords_filename, 'r', encoding='utf-8') as s:
        stopwords = s.read()
        stopwords_list = stopwords.split('\n')
    
    print("----------进行词频统计中，请稍等----------")
    word_count = {}
    for word in wordlist:                               #过滤停用词并且统计词频
        if word not in stopwords_list:
            count = word_count.get(word, 0)
            word_count[word] = count + 1
    word_count_sorted = collections.OrderedDict(sorted(word_count.items(), key=lambda dc:dc[1],reverse=True))

    keys = list(word_count_sorted.keys())               #观察高频词、低频词，设定词频前(后)30为高(低)频词
    print("----------高频词如下----------")
    print(keys[:30:])
    print("----------低频词如下----------")
    print(keys[-30::])

    word_feature = {}
    for key in word_count_sorted:
        if word_count_sorted[key] >= n:                 #过滤低频词（出现次数低于给定值n）
            word_feature[key] = word_count_sorted[key]
    word_pack = list(word_feature.keys()) 
    print("----------特征词集下----------")
    print(word_pack)

    return word_feature, word_pack

def TF_IDF(danmulist, wordlist, stopwords_filename):
    """
    特征词获取函数：利用TF-IDF方法获取特征词
    """
    with open(stopwords_filename, 'r', encoding='utf-8') as s:
        stopwords = s.read()
        stopwords_list = stopwords.split('\n')

    print("----------进行特征词获取中，请稍等----------")
    word_count = {}
    for word in wordlist:                               #过滤停用词并且统计词频
        if word not in stopwords_list:
            count = word_count.get(word, 0)
            word_count[word] = count + 1

    word_tf = {}                                        #计算每个词的TF值
    for i in word_count:
        word_tf[i] = word_count[i]/sum(word_count.values())
    
    num = len(danmulist)                                #计算每个词的IDF值
    word_idf = {}
    word_danmu = collections.defaultdict(int)
    for i in word_count:
        for j in danmulist:
            if i in j:
                word_danmu[i] += 1
    for i in word_count:
        word_idf[i] = math.log(num/(word_danmu[i]+1))

    word_tf_idf = {}                                    #计算每个词的TF*IDF的值
    for i in word_count:
        word_tf_idf[i] = word_tf[i]*word_idf[i]
 
    # 对字典按值由大到小排序
    word_feature = collections.OrderedDict(sorted(word_tf_idf.items(), key=lambda dc:dc[1],reverse=True))
    
    word_pack = list(word_feature.keys())
    print(word_pack[:50:])                              #取前50个作为特征词

    return word_pack

def draw_cloud(word_feature):
    """
    词云图绘制函数：用于绘制高频词的词云图
    """
    print("----------绘制词云图中，请稍等----------")
    img = Image.open("爱心.png")
    img_mask = np.array(img)
    image_colors = ImageColorGenerator(img_mask)

    wc = WordCloud(font_path="simhei.ttf", mask=img_mask, background_color="white", max_words=300, max_font_size=150)
    wc.generate_from_frequencies(word_feature)

    plt.imshow(wc.recolor(color_func=image_colors), interpolation='bilinear')
    plt.axis('off')
    plt.show()

def get_onehot_matrix(danmulist, word_pack):
    """
    得到one-hot矩阵函数：得到弹幕的onehot的矩阵（过滤掉了短的弹幕）
    """
    print("----------计算one-hot矩阵中，请稍等----------")
    #danmulist = list(set(danmulist))                   #去掉重复的弹幕
    lis = []
    danmulist_new = []
    for danmu in danmulist:                             #得到one-hot矩阵
        vector = [0] * len(word_pack)
        if len(danmu) >= 10:                            #过滤短的弹幕
            seg_list = jieba.cut(danmu, cut_all=False)
            for word in seg_list:
                if word in word_pack:
                    vector[word_pack.index(word)] = 1
            lis.append(vector)
            danmulist_new.append(danmu)
    matrix = np.array(lis)
    return danmulist_new, matrix

def danmu_compare(danmulist, matrix):
    """
    比较弹幕语义函数：随机找到一条弹幕，寻找与其语义最接近的和最远的弹幕，进行比较
    """
    print("----------正在比较弹幕文义----------")
    index = random.randint(0,len(danmulist)-1)
    while(np.all(matrix[index]==0)):
        index = random.randint(0,len(danmulist)-1)
    print("----------随机找到的弹幕是----------")
    print("编号为:", index, "内容是:", danmulist[index])
    vector = matrix[index]

    dis_list = []
    for row in range(0, len(matrix)):                   #计算各向量与该向量的距离
        if row != index:
            dis = np.sqrt(np.sum(np.square(vector - matrix[row])))
            dis_list.append(dis)
    index_min = dis_list.index(min(dis_list))
    index_max = dis_list.index(max(dis_list))

    print("----------与其语义内容最近的弹幕内容是----------")
    if index_min < index:
        print("编号为:", index_min, "内容是:", danmulist[index_min])
    else:
        print("编号为:", index_min+1, "内容是:", danmulist[index_min+1])
    print("----------与其语义内容最远的弹幕内容是----------")
    print("编号为:", index_max, "内容是:", danmulist[index_max])

def get_danmu_feature(danmulist, matrix):
    """
    得到最具代表性的弹幕函数：找到矩阵的重心，离重心最近的向量即最具代表性的弹幕
    """
    print("----------正在找最具有代表性的弹幕，请稍等----------")
    count = [0] * len(matrix[0])                        #计算矩阵重心
    for row in range(0, len(matrix)):
        for column in range(0, len(matrix[0])):
            count[column] += matrix[row][column]
    for column in range(0, len(count)):
        count[column] = count[column] / len(matrix)
    gravity = count
    
    dis_list = []
    for row in range(0, len(matrix)):                   #计算各向量与重心的距离
        dis = np.sqrt(np.sum(np.square(gravity - matrix[row])))
        dis_list.append(dis)

    dm_index_min = dis_list.index(min(dis_list))

    print("----------最具代表性的弹幕内容是----------")
    print(danmulist[dm_index_min])
 
def training(danmulist, stopwords):
    """
    深度学习词向量表征：用gensim中的word2vec去构建词向量
    """
    jieba.load_userdict(stopwords)                      #添加停用词进自定义字典

    with open(stopwords, 'r', encoding='utf-8') as s:
        stopwords = s.read()
        stopwords_list = stopwords.split('\n')
    
    print("----------进行分词中，请稍等----------")
    danmu = []
    for sen in danmulist:
        seg_list = jieba.cut(sen, cut_all=False)        #分词
        danmu.append(seg_list)

    f = open("danmulist.txt","w",encoding="utf-8")
    for line in danmu:
        for word in line:
            if word not in stopwords_list:
                f.write(word + ' ')
        f.write("\n")
    f.close()

    #使用LineSentence函数处理语料，可避免前期构建语料的复杂性
    model = Word2Vec(LineSentence(open('danmulist.txt', "r",encoding='UTF-8')),
                     sg=0,
                     vector_size=192, 
                     window=5, 
                     min_count=5, 
                     workers=8
                    )
    
    #模型保存
    model.save('danmu.model')

    word = "粉"
    print("----------输出与粉最相似的十个词----------")
    if word in model.wv.index_to_key:
        print(model.wv.most_similar(word))

if __name__ == '__main__':                                                                                                             
    danmulist = read_document("danmuku.csv")                                        #读取文档
    wordlist = cut_word(danmulist, "stopwords_list.txt")                            #分词
    word_feature, word_pack = word_analyse(wordlist, "stopwords_list.txt", 5000)    #分析词频
    #word_pack = TF_IDF(danmulist, wordlist, "stopwords_list.txt")                   #用TF-IDF得到特征词
    draw_cloud(word_feature)                                                        #绘制词云图
    danmulist_new, matrix = get_onehot_matrix(danmulist, word_pack)                 #得到弹幕one-hot矩阵
    danmu_compare(danmulist_new, matrix)                                            #分析弹幕语义相似度
    get_danmu_feature(danmulist_new, matrix)                                        #得到最具代表性的弹幕
    #training(danmulist, "stopwords_list.txt")                                       #word2vec词向量表征