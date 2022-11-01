import math
import numpy as np
from PIL import Image

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
walk1 = list(random_walk(1, 1, 0.01, 10))
walk2 = list(random_walk(1, 1, 25, 10))
walk3 = list(random_walk(1, 1, 100, 10))

for i in zip(walk1, walk2, walk3):
    print(i)
'''

# 设计FaceDataset类，实现图片数据的加载
class FaceDataset():
    def __init__(self, filepath):
        self.pathlist = filepath
    
    def process(self):
        image = Image.open(self.path)
        image_array = np.array(image)
        print(image_array)
        return image_array
    
    def __iter__(self):
        return self

    def __next__(self):
        self.path = self.path_shape()