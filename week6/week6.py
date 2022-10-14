import os
from PIL import Image
from PIL import ImageFilter
from matplotlib import pyplot as plt

#实现基类
class Filter:
    def __init__(self, path, *plist):
        """
        两个数据属性
        image:待处理的图片实例，即PIL库的Image实例
        plist:参数列表，用以存储可能使用参数的滤波器的参数
        """
        self._image = Image.open(path)
        self._plist = plist
    
    def filter(self):
        """
        能够对Image实例的特定处理，在子类中具体实现
        """
        pass

#实现四个子类，filter()方法进行实现
class FIND_EDGES_Filter(Filter):
    '''
    提取边缘
    '''
    def __init__(self, path, *plist):
        super().__init__(path, plist)
    
    def filter(self):
        image_filter = self._image.filter(ImageFilter.FIND_EDGES)
        return image_filter

class SHARPEN_Filter(Filter):
    '''
    锐化
    '''
    def __init__(self, path, *plist):
        super().__init__(path, plist)
    
    def filter(self):
        image_filter = self._image.filter(ImageFilter.SHARPEN)
        return image_filter

class BLUR_Filter(Filter):
    '''
    模糊
    '''
    def __init__(self, path, *plist):
        super().__init__(path, plist)
    
    def filter(self):
        image_filter = self._image.filter(ImageFilter.BLUR)
        return image_filter

class RESIZE_Filter(Filter):
    '''
    大小调整
    '''
    def __init__(self, path, *plist):
        super().__init__(path, plist)
    
    def filter(self):
        w,h = self._image.size
        wrate = self._plist[0]
        hrate = self._plist[1]
        image_filter = self._image.resize((int(w*wrate),int(h*hrate)))
        return image_filter

#实现类ImageShop,实现具体批量处理图片类
class ImageShop:
    def __init__(self, formation, filepath):
        """
        三个数据属性
        formation:图片格式
        filepath:图片文件（应该支持目录）
        imglist:存储待处理图片列表
        imgpro:储存处理后的图片列表
        """
        self._formation = formation
        self._filepath = filepath
        self._imglist = []
        self._imgpro = []

    def load_images(self):
        """
        从路径加载特定格式的图片
        """
        dirs = os.listdir(self._filepath)                           # 获取指定路径下的文件
        for path in dirs:
            if os.path.splitext(path)[1] == self._formation:        # 加载目录中的所有特定格式图片
                img = Filter(self._filepath + '/' + path)
                self._imglist.append(img)                           # 以Fliter类储存

    def __batch_ps(self, Filter, *plist):
        """
        处理图片的内部方法，利用某个过滤器(Filter)对所有图片进行处理
        """
        for i in range(len(self._imgpro)):
            img = self._imgpro[i]
            img._plist = plist                                      # 更新参数属性
            img_pro = Filter.filter(img)                            # 处理图片
            img._image = img_pro                                    # 更新处理的图片

    def batch_ps(self, *args):
        """
        批量处理图片的对外公开方法，可以同时进行若干操作
        args:不定长操作参数，参数按一种特定格式的tuple输入，比如（操作名，参数）
        """
        self._imgpro = self._imglist                                # 初始化处理后的图片列表
        for op in args:
            if op == 'find_edges':
                self.__batch_ps(FIND_EDGES_Filter)
            elif op == 'sharpen':
                self.__batch_ps(SHARPEN_Filter)
            elif op == 'blur':
                self.__batch_ps(BLUR_Filter)
            elif op[0] == 'resize':
                self.__batch_ps(RESIZE_Filter, *op[1:])
            else:
                print("Error, do not find operation named {}.".format(op[0]))
                break
        
    def display(self, row=5, col=5, max_num=100):
        """
        处理效果显示
        row&col:图片呈现可能需要行和列
        max_num:最多显示多少张
        """
        if len(self._imgpro) > max_num:                                 # 控制最大显示图片数
            self._imgpro = self._imgpro[:max_num]
        for num in range(0,len(self._imgpro), row*col):
            for i in range(row*col):                                    # 控制每张子图展示图片数量
                if num + i < len(self._imgpro):
                    img = self._imgpro[num+i]
                    plt.subplot(row, col, i+1)
                    plt.imshow(img._image)
            plt.show()

    def save(self, path, formation = '.png'):
        """
        处理结果输出
        path:输出路径
        formation:输出格式，默认为png
        """
        for i in range(len(self._imgpro)):
            img = self._imgpro[i]
            img._image.save(path+str(i+1)+formation)

#实现测试类TestImageShop，实现对ImageShop类的测试
class TestImageShop:
    def __init__(self, formation, filepath):
        self._test = ImageShop(formation, filepath)
        self._test.load_images()

    def text_imageshop(self, *args):
        self._test.batch_ps(*args)
        self._test.display(2, 2)
        self._test.save('week6/photo_fliter/')

def main():
    formation = '.png'
    filepath = 'week6/photo'

    T = TestImageShop(formation, filepath)
    T.text_imageshop('sharpen','find_edges')
    #T.text_imageshop('blur', ('resize', 0.5, 0.5))

if __name__ == '__main__': main()