import os
import sys
import math
import numpy as np
from PIL import Image
from PIL import ImageFile
from memory_profiler import profile

'''
# 实现random_walk生成器
def random_walk(mu, x, sigma_square, N):
    for i in range(N):
        yield x
        w_t = np.random.normal(0,math.sqrt(sigma_square))
        x = mu + x + w_t

# 测试
for i in random_walk(1, 1, 4, 10):
    print(i)

# 实现多维随机游走序列生成器
def random_walk_vector(*walk):
    return zip(*walk)

# 测试
walk1 = random_walk(1, 1, 0.01, 10)
walk2 = random_walk(1, 1, 25, 10)
walk3 = random_walk(1, 1, 100, 10)
walk_vec = random_walk_vector(walk1, walk2, walk3)
for vec in walk_vec:
    print(vec)
'''

# 设计FaceDataset类，实现图片数据的加载
class FaceDataset():
    def __init__(self, index=0, max=sys.maxsize):
        self._pathlist = []
        self._index = index                                         # 从第几张开始加载
        self._max = max                                             # 最多加载多少张
    
    def load_path(self, path_dir):
        print("-----开始加载图片路径-----")
        for root, dirs, files in os.walk(path_dir):                 # 生成器，遍历目录
            for name in files:
                self._pathlist.append(os.path.join(root, name))
        print(f"-----图片路径加载完成，共{len(self._pathlist)}张图片-----")
        if self._max > len(self._pathlist):
            self._max = len(self._pathlist)
        self._path = self._pathlist[0]

    def process(self):
        ImageFile.LOAD_TRUNCATED_IMAGES = True                      # 当遇到数据截断的图片时，PIL不报错，进行下一个
        image = Image.open(self._path)
        image_array = np.array(image)
        return image_array
    
    def __iter__(self):
        return self

    def __next__(self):
        if self._index+1 <= self._max:
            self._path = self._pathlist[self._index]
            self._index += 1
            return self.process()
        else:
            raise StopIteration('{}张图片已处理完毕'.format(self._max))

# 测试
@ profile()
def normal_process():
    path_dir = 'week9/originalPics'
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    for root, dirs, files in os.walk(path_dir):
            for name in files:
                path = os.path.join(root, name)
                image = Image.open(path)
                image_array = np.array(image)
                print(image_array)

@ profile()
def iterable_process():
    path_dir = 'week9/originalPics'
    face = FaceDataset()
    face.load_path(path_dir)
    for img in face:
        print(img)
        #pass

#normal_process()
iterable_process()