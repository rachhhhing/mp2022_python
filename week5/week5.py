import re
import jieba
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

class Tokenizer:
    def __init__(self, chars, coding='c', PDA=0):
        """
        初始化函数：初始化类，并且构建编码词典
        """
        self._chars = chars
        self._coding = coding
        self._PDA = PDA

        dic = {}
        dic['[PAD]'] = PDA
        i = 0                                   #从0开始编码
        if coding=='c':
            for char in chars:
                for ch in char:
                    if ch not in dic.keys():
                        if i == PDA: i+=1       #跳过PDA的值
                        dic[ch] = i; i+=1
        elif coding=='w':
            for char in chars:
                for ch in jieba.lcut(char):
                    if ch not in dic.keys():
                        if i == PDA: i+=1
                        dic[ch] = i; i+=1
        self._dic = dic
    
    def tokenize(self, sentence):
        """
        分词（字）函数：输入一句话，返回分词（字）后的字符列表
        """
        list_of_chars = []
        if self._coding == 'c':
            for char in sentence:
                list_of_chars.append(char)
        elif self._coding == 'w':
            list_of_chars = jieba.lcut(sentence)
        return list_of_chars
    
    def encode(self, list_of_chars):
        """
        编码函数：输入字符列表，返回转化后的数字列表
        """
        tokens = []
        for char in list_of_chars:
            tokens.append(self._dic[char])
        return tokens

    def get_seq_len(self):
        """
        得长函数:观察句子长度分布，确定一个合适的seq_len
        """
        text = self._chars
        text_len = []
        if self._coding == 'c':
            for txt in text:
                text_len.append(len(txt))
        elif self._coding  == 'w':
            for txt in text:
                text_len.append(len(jieba.lcut(txt)))
        sns.distplot(text_len)
        plt.title('text length distribution_{}'.format(self._coding))		# 标题
        plt.xlabel('length')                                        		# x轴名
        #plt.savefig('text length distribution_{}.png'.format(self._coding))
        plt.show()
        seq_len = np.percentile(text_len, 75)		#用75%分位数作为seq_len的值
        return int(seq_len)

    def trim(self, tokens, seq_len):
        """
        整长函数：输入数字列表tokens，整理数字列表的长度。不足seq_len的部分用PAD补足，超过的部分截断。
        """
        if len(tokens) >= seq_len:
            return tokens[:seq_len]
        else:
            add_len = seq_len - len(tokens)
            tokens_trim = tokens + [self._PDA]*add_len
            return tokens_trim
    
    def decode(self, tokens):
        """
        翻译函数：将模型输出的数字列表翻译回句子，如果有PAD，输出'[PAD]'
        """
        key = list(self._dic.keys())
        value = list(self._dic.values())
        chars = []
        for code in tokens:
            if code == self._PDA:
                chars.append('[PDA]')
                break
            else:
                ch = key[value.index(code)]
                chars.append(ch)
        print("".join(chars))
    
    def encode_all(self, seq_len):
        """
        编码文本：返回所有文本(chars)的长度为seq_len的tokens
        """
        tokens_list = []
        for sen in self._chars:
            sen_token = self.trim(self.encode(self.tokenize(sen)), seq_len)
            tokens_list.append(sen_token)
        return tokens_list

def cleanword(filename):
    """
    清洗文本函数：预处理数据文件，洗出微博内容
    """       
    with open(filename,'r',encoding='utf-8') as f:
        data = pd.read_csv(f, dtype=str, delimiter="\t")
        for i in range(len(data)):
            text = data.iloc[i,1]                       # 读取微博text
            try:
                text = re.sub(r"(回复)?(//)?\s*@\S*?\s*(:| |$)", " ", text)  # 去除正文中的@和回复/转发中的用户名
                text = re.sub(r'http[:.]+\S+', '', text)    # 除去url
                text = text.replace("我在:", "")            # 去除无意义的词语
                text = text.replace("我在这里:","")
                text = re.sub(r"\s+", " ", text)            # 合并正文中过多的空格
                file = open('week5/clean_text.txt','a',encoding='utf-8')
                file.write(text+'\n')
            except:
                continue
        
def main():
    #cleanword('week5/final_none_duplicate.txt')         #数据预处理，得到清洗的文本
    with open('week5/clean_text.txt','r',encoding='utf-8') as f:
        text = f.read().splitlines()
        text = list(filter(None, text))                 #去除空值
    T = Tokenizer(text)
    #T = Tokenizer(text,'w')
    #print(T._dic)
    #seq_len = T.get_seq_len()
    #print(seq_len)
    
    '''
    print("-----长度大于seq_len-----")
    txt = text[0]
    print("#text#")
    print(txt)
    print("#encode#" )
    code = T.trim(T.encode(T.tokenize(txt)), seq_len)
    print(code)
    print("#decode#" )
    T.decode(code)
    print("-----长度小于seq_len-----")
    txt = text[1]
    print("#text#")
    print(txt)
    print("#encode#" )
    code = T.trim(T.encode(T.tokenize(txt)), seq_len)
    print(code)
    print("#decode#" )
    T.decode(code)
    '''

    #print(T.encode_all(seq_len))

if __name__ == '__main__': main()