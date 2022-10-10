import os
from PIL import Image
from PIL import ImageFilter
from matplotlib import pyplot as plt

#ʵ�ֻ���
class Filter:
    def __init__(self, path):
        """
        ������������
        image:�������ͼƬʵ������PIL���Imageʵ��
        plist:�����б����Դ洢����ʹ�ò������˲����Ĳ���
        """
        self._image = Image.open(path)
        self._plist = []
    
    def filter(self):
        """
        �ܹ���Imageʵ�����ض�����
        """
        pass

#ʵ���ĸ����࣬filter()��������ʵ��
class FIND_EDGES_Filter(Filter):
    '''
    ��ȡ��Ե
    '''
    def __init__(self,path):
        super().__init__(self, path)
    
    def filter(self):
        image_filter = self._image.filter(ImageFilter.FIND_EDGES)
        return image_filter

class Sharpen_Filter(Filter):
    '''
    ��
    '''
    def __init__(self,path):
        super().__init__(self, path)
    
    def filter(self):
        image_filter = self._image.filter(ImageFilter.Sharpen)
        return image_filter

class Blur_Filter(Filter):
    '''
    ģ��
    '''
    def __init__(self,path):
        super().__init__(self, path)
    
    def filter(self):
        image_filter = self._image.filter(ImageFilter.Blur)
        return image_filter

class Resize_Filter(Filter):
    '''
    ��С����
    '''
    def __init__(self, path, width_rate, hight_rate):
        super().__init__(self, path)
        self._wrate = width_rate
        self._hrate = hight_rate
    
    def filter(self):
        w,h = self._image.size
        image_filter = self._image.resize((int(w*self._wrate),int(h*self._hrate)))
        return image_filter

#ʵ����ImageShop,ʵ�־�����������ͼƬ��
class ImageShop(Filter):
    def __init__(self, formation, file_path, image_list, image_process):
        """
        �ĸ���������
        formation:ͼƬ��ʽ
        file_path:ͼƬ�ļ���Ӧ��֧��Ŀ¼��
        image_list:�洢ͼƬʵ��(Imageʵ��)���б�
        image_process���洢�������ͼƬ
        """
        self._formation = formation
        self._filepath = file_path
        self._imglist = image_list
        self._imgpro = image_process

    def load_images(self):
        """
        ��·�������ض���ʽ��ͼƬ
        """
        dirs = os.listdir(self._filepath)                           # ��ȡָ��·���µ��ļ�
        for path in dirs:
            if os.path.splitext(path)[1] == self._formation:        # ����Ŀ¼�е������ض���ʽͼƬ
                image = Image.open(path)
                self._imglist.append(img)

    def __batch_ps(self, Filter):
        """
        ����ĳ��������������ͼƬ���д���
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