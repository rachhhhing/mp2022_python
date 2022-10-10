import os
from PIL import Image
from PIL import ImageFilter
from matplotlib import pyplot as plt

#实现基类
class Filter:
    def __init__(self, path):
        """
        两个数据属性
        image:待处理的图片实例，即PIL库的Image实例
        plist:参数列表，用以存储可能使用参数的滤波器的参数
        """
        self._image = Image.open(path)
        self._plist = []
    
    def filter(self):
        """
        能够对Image实例的特定处理
        """
        pass

#实现四个子类，filter()方法进行实现
class FIND_EDGES_Filter(Filter):
    '''
    提取边缘
    '''
    def __init__(self,path):
        super().__init__(self, path)
    
    def filter(self):
        image_filter = self._image.filter(ImageFilter.FIND_EDGES)
        return image_filter

class Sharpen_Filter(Filter):
    '''
    锐化
    '''
    def __init__(self,path):
        super().__init__(self, path)
    
    def filter(self):
        image_filter = self._image.filter(ImageFilter.Sharpen)
        return image_filter

class Blur_Filter(Filter):
    '''
    模糊
    '''
    def __init__(self,path):
        super().__init__(self, path)
    
    def filter(self):
        image_filter = self._image.filter(ImageFilter.Blur)
        return image_filter

class Resize_Filter(Filter):
    '''
    大小调整
    '''
    def __init__(self, path, width_rate, hight_rate):
        super().__init__(self, path)
        self._wrate = width_rate
        self._hrate = hight_rate
    
    def filter(self):
        w,h = self._image.size
        image_filter = self._image.resize((int(w*self._wrate),int(h*self._hrate)))
        return image_filter

#实现类ImageShop,实现具体批量处理图片类
class ImageShop(Filter):
    def __init__(self, formation, file_path, image_list, image_process):
        """
        四个数据属性
        formation:图片格式
        file_path:图片文件（应该支持目录）
        image_list:存储图片实例(Image实例)的列表
        image_process：存储处理过的图片
        """
        self._formation = formation
        self._filepath = file_path
        self._imglist = image_list
        self._imgpro = image_process

    def load_images(self):
        """
        从路径加载特定格式的图片
        """
        dirs = os.listdir(self._filepath)                           # 获取指定路径下的文件
        for path in dirs:
            if os.path.splitext(path)[1] == self._formation:        # 加载目录中的所有特定格式图片
                image = Image.open(path)
                self._imglist.append(img)

    def __batch_ps(self, Filter):
        """
        利用某个过滤器对所有图片进行处理
        """
        for img in self._imglist:
            img_pro = Filter.filter(img)
            self.imgpro[each] = img
        for i in self.Image_list:
            Image_p = FIND_EDGES_Filter(self.path)
            Image_p = Image_p.filter(i)
            self.Image_process.append(Image_p)

    def batch_ps(self,w_rate,h_rate,*args):
        for i in range(len(self.Image_list)):
            if args[0] == '1':
                Image_t = FIND_EDGES_Filter(self.path_list[i])
                Image_t = Image_t.filter(Image_list[i])
                self.Image_process.append(Image_t)
            if args[0] == '2':
                Image_t = EDGE_ENHANCE_Filter(self.path_list[i])
                Image_t = Image_t.filter(Image_list[i])
                self.Image_process.append(Image_t)
            if args[0] == '3':
                Image_t = GaussianBlur_Filter(self.path_list[i])
                Image_t = Image_t.filter(Image_list[i])
                self.Image_process.append(Image_t)
            if args[0] == '4':
                Image_t = new_Filter(self.path_list[i],w_rate,h_rate)
                Image_t = Image_t.filter(Image_list[i])
                self.Image_process.append(Image_t)

    def display(self,row,col):
        num = len(self.Image_process)
        for i in range(num):
            plt.subplot(row,col,i+1)
            plt.imshow(self.Image_process[i])
        plt.show()

    def save(self,path,formation):
        for i in range(len(self.Image_process)):
            self.Image_process[i].save(path+str(i+1)+'p'+'.'+formation)