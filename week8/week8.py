import os
import sys
import time
import random
import pysnooper
from tqdm import tqdm
from functools import wraps
from playsound import playsound
from memory_profiler import profile
from line_profiler import LineProfiler

'''
# 用函数实现文件路径检查装饰器
def path_examine(path):
    def decorator(func):
        @ wraps(func)
        def wrapper(*args, **kwargs):
            if os.path.exists(path) == False:       # 检查路径是否存在
                print('The path does not exist! We creat for you.')
                os.mkdir(path)                      # 创建对应文件夹
            return func(*args,**kwargs)
        return wrapper
    return decorator

# 测试
path = 'test'
@ path_examine(path)

def test(path):
    print(os.path.exists(path))
test(path)
'''

'''
# 用类实现声音提醒函数结束装饰器
class End_Music:
    def __init__(self):
        self.music_path_int = 'D:/code/mp2022/week8/music/int.mp3'
        self.music_path_list = 'D:/code/mp2022/week8/music/list.mp3'
        self.music_path_tuple = 'D:/code/mp2022/week8/music/tuple.mp3'
    
    def __call__(self, func):
        @ wraps(func)
        def wrapper(*args, **kwargs):
            ans_list = func(*args, **kwargs)
            for ans in ans_list:
                if isinstance(ans, int):
                    playsound(self.music_path_int)
                elif isinstance(ans, list):
                    playsound(self.music_path_list)
                elif isinstance(ans, tuple):
                    playsound(self.music_path_tuple)
            return ans_list
        return wrapper

# 测试
@ End_Music()
def test():
    return 1, [1,2], (1,2)
test()
'''

'''
# 用函数实现保存输出装饰器
def save_print(save_path):
    def decorator(func):
        @ wraps(func)
        def wrapper(*args, **kwargs):
            sys.stdout = open(save_path, 'w')
            return func(*args, **kwargs)
        return wrapper
    return decorator

# 测试
@ save_print('week8/save_print.txt')
def test():
    print('1')
    print('2')
    print('3')
test()
'''

'''
# 用类模拟耗时耗内存的操作
# 这里用生成一个大字典（结构为"ID:成绩"）模拟耗内存操作，用遍历字典查询考某成绩的学生模拟耗时操作
class Grade:
    def __init__(self):
        self.dic = {}

    @ profile                                   # memory profile
    @ pysnooper.snoop('week8/dic.log')          # pysnooper
    def input_grade(self):
        """
        录入成绩的方法，即生成大字典，模拟耗内存操作
        """
        for i in range(10 ** 2):
            self.dic[i] = random.randint(0,100)
    
    def search(self, grade):
        """
        查询成绩的方法，即遍历大字典，模拟耗时操作
        """
        stu = []
        for key in tqdm(self.dic):              # tqdm
            time.sleep(0.000001)
            if self.dic[key] == grade:
                stu.append(key)
        return stu

# 测试
g = Grade()
g.input_grade()

lp = LineProfiler()                             # line profile
lp.enable_by_count()
lp_wrapper = lp(g.search)
stu = g.search(90)
lp.print_stats()
'''