import os
import abc
import jieba
import imageio
import librosa
import numpy as np
import seaborn as sns
from PIL import Image 
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from wordcloud import WordCloud, ImageColorGenerator

# 抽象类
class Plotter(abc.ABC):
    @abc.abstractmethod
    def plot(self,*arg,**kwargs):
        pass

# 点型数据绘制
class PointPlotter(Plotter):
    def __init__(self, point):
        self._point = point

    def plot(self):
        for x,y in self._point:
            plt.scatter(x,y)
        plt.show()

# 2维或3维数组型数据绘制
class ArrayPlotter(Plotter):
    def __init__(self, array):
        self._array = array

    def plot(self):
        if len(self._array) == 2:
            plt.scatter(self._array[0], self._array[1])
            plt.show()
        elif len(self._array) == 3:
            ax = plt.subplot(projection = '3d')
            ax.scatter(self._array[0], self._array[1], self._array[2])
            plt.show()
        else:
            print(f"不支持{len(self._array)}数组绘制")

# 文本型数据绘制
class TextPlotter(Plotter):
    def __init__(self, text):
        self._text = text

    def plot(self):
        wordlist = []
        for sen in self._text:
            seg_list = jieba.cut(sen, cut_all=False)
            wordlist.extend(seg_list)
        txt = ' '.join(wordlist)                    # generate需要string
        
        img = Image.open("week10/爱心.png")
        img_mask = np.array(img)
        image_colors = ImageColorGenerator(img_mask)

        wc = WordCloud(font_path="simhei.ttf", 
                    mask=img_mask, 
                    background_color="white", 
                    max_words=300, 
                    max_font_size=150)
        wc.generate(txt)                            # 会自动根据词频形成词云图

        plt.imshow(wc.recolor(color_func=image_colors), interpolation='bilinear')
        plt.axis('off')
        plt.show()

# 图像型数据绘制
class ImagePlotter(Plotter):
    def __init__(self, image):
        self._image = []
        for each in image:
            if isinstance(each, str):               # 判断是否是路径
                img = Image.open(each)
                self._image.append(img)
            else:
                self._image.append(each)

    def plot(self, row=2, col=2):
        for num in range(0,len(self._image), row*col):
            for i in range(row*col):
                if num + i < len(self._image):
                    img = self._image[num+i]
                    plt.subplot(row, col, i+1)
                    plt.imshow(img)
            plt.show()
        
# 图片序列的可视化
class GifPlotter(Plotter):
    def __init__(self, image):
        self._image = []
        for each in image:
            if isinstance(each, str):               # 判断是否是路径
                img = imageio.imread(each)
                self._image.append(img)
            else:
                self._image.append(each)

    def plot(self, save_path='week10/GifPlotter.gif', duration=0.5):
        imageio.mimsave(save_path, self._image, 'GIF', duration=duration)

# 超过3维数组可视化
class KeyFeaturePlotter(Plotter):
    def __init__(self, array):
        self._array = array

    def plot(self):
        if len(self._array) <= 3:
            print(f"不支持{len(self._array)}数组绘制")
        else:
            pca = PCA(n_components=2)               # 降到2维
            pca.fit(self._array)
            array = pca.transform(self._array)      # 降维后结果
            for point in array:
                plt.scatter(point[0], point[1])
            plt.show()

# 音频数据绘制
class MusicPlotter(Plotter):
    def __init__(self, music):
        self._music = music

    def plot(self):
        x , sr = librosa.load(self._music)
        #print(type(x), type(sr))  
        #plt.figure(figsize=(10, 5))
        librosa.display.waveplot(x, sr=sr)
        plt.show()
    
def main():
    '''
    # 点型数据绘制
    point = [(1,1),(2,2),(3,3),(4,4),(5,5)]
    pointplt = PointPlotter(point)
    pointplt.plot()
    '''

    '''
    # 数组型数据绘制
    array = [[1,2,3,4,5],[1,2,3,4,5],[1,2,3,4,5]]
    arrayplt = ArrayPlotter(array)
    arrayplt.plot()
    '''

    '''
    # 文本型数据绘制
    with open('week10/spring.txt') as f:
        text = f.readlines()
    textplt = TextPlotter(text)
    textplt.plot()
    '''

    '''
    # 图片型数据绘制
    image = []
    for root, dirs, files in os.walk('week10/photo'):
        for f in files:
            #image.append(os.path.join(root,f))
            img = Image.open(os.path.join(root,f))
            image.append(img)
    imageplt = ImagePlotter(image)
    imageplt.plot()
    '''

    '''
    # 图片序列的可视化
    image = []
    for root, dirs, files in os.walk('week10\photo'):
        for f in files:
            #image.append(os.path.join(root,f))
            try:
                img = imageio.imread(os.path.join(root,f))
                image.append(img)
            except:
                pass
    gifplt = GifPlotter(image)
    gifplt.plot()
    '''

    '''
    # 超过三维的多维数组绘制
    data = sns.load_dataset("iris")                 # 用的是著名的鸢尾花的数据
    data = data[(data['species']=='setosa') | (data['species']=='virginica')]
    array = data.iloc[:, :4]
    keyfeatureplt = KeyFeaturePlotter(array)
    keyfeatureplt.plot()
    '''

    # 音频数据绘制
    music = 

if __name__ == '__main__': main()