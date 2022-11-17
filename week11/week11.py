from multiprocessing import Process

class Map(Process):
    '''
    Map进程读取文档路径并进行词频统计，返回该文本的词频统计结果。
    '''
    def __init__(self,name,step,lock,content_path = "content.pkl"):
        super().__init__()
        self._name = name
        self._content = lock_task1(lock,step,content_path)
    
    @property
    def name(self):
        return self._name

    def run(self):
        count_dict = {}
        for content in self._content:
            line_cut = jieba.lcut(content)
            for word in line_cut:
                if word not in punctuation:
                    if word in count_dict:
                        count_dict[word] += 1
                    else:
                        count_dict[word] = 1
        with open(self._name + ".pkl",'wb') as f:
            pickle.dump(count_dict,f)
    