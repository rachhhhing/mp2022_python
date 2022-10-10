import re
import jieba
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

class Tokenizer:
    def __init__(self, chars, coding='c', PDA=0):
        """
        ��ʼ����������ʼ���࣬���ҹ�������ʵ�
        """
        self._chars = chars
        self._coding = coding
        self._PDA = PDA

        dic = {}
        dic['[PAD]'] = PDA
        i = 0                                   #��0��ʼ����
        if coding=='c':
            for char in chars:
                for ch in char:
                    if ch not in dic.keys():
                        if i == PDA: i+=1       #����PDA��ֵ
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
        �ִʣ��֣�����������һ�仰�����طִʣ��֣�����ַ��б�
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
        ���뺯���������ַ��б�����ת����������б�
        """
        tokens = []
        for char in list_of_chars:
            tokens.append(self._dic[char])
        return tokens

    def get_seq_len(self):
        """
        �ó�����:�۲���ӳ��ȷֲ���ȷ��һ�����ʵ�seq_len
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
        plt.title('text length distribution_{}'.format(self._coding))		# ����
        plt.xlabel('length')                                        		# x����
        #plt.savefig('text length distribution_{}.png'.format(self._coding))
        plt.show()
        seq_len = np.percentile(text_len, 75)		#��75%��λ����Ϊseq_len��ֵ
        return int(seq_len)

    def trim(self, tokens, seq_len):
        """
        �������������������б�tokens�����������б�ĳ��ȡ�����seq_len�Ĳ�����PAD���㣬�����Ĳ��ֽضϡ�
        """
        if len(tokens) >= seq_len:
            return tokens[:seq_len]
        else:
            add_len = seq_len - len(tokens)
            tokens_trim = tokens + [self._PDA]*add_len
            return tokens_trim
    
    def decode(self, tokens):
        """
        ���뺯������ģ������������б���ؾ��ӣ������PAD�����'[PAD]'
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
        �����ı������������ı�(chars)�ĳ���Ϊseq_len��tokens
        """
        tokens_list = []
        for sen in self._chars:
            sen_token = self.trim(self.encode(self.tokenize(sen)), seq_len)
            tokens_list.append(sen_token)
        return tokens_list

def cleanword(filename):
    """
    ��ϴ�ı�������Ԥ���������ļ���ϴ��΢������
    """       
    with open(filename,'r',encoding='utf-8') as f:
        data = pd.read_csv(f, dtype=str, delimiter="\t")
        for i in range(len(data)):
            text = data.iloc[i,1]                       # ��ȡ΢��text
            try:
                text = re.sub(r"(�ظ�)?(//)?\s*@\S*?\s*(:| |$)", " ", text)  # ȥ�������е�@�ͻظ�/ת���е��û���
                text = re.sub(r'http[:.]+\S+', '', text)    # ��ȥurl
                text = text.replace("����:", "")            # ȥ��������Ĵ���
                text = text.replace("��������:","")
                text = re.sub(r"\s+", " ", text)            # �ϲ������й���Ŀո�
                file = open('week5/clean_text.txt','a',encoding='utf-8')
                file.write(text+'\n')
            except:
                continue
        
def main():
    #cleanword('week5/final_none_duplicate.txt')         #����Ԥ�����õ���ϴ���ı�
    with open('week5/clean_text.txt','r',encoding='utf-8') as f:
        text = f.read().splitlines()
        text = list(filter(None, text))                 #ȥ����ֵ
    T = Tokenizer(text)
    #T = Tokenizer(text,'w')
    #print(T._dic)
    #seq_len = T.get_seq_len()
    #print(seq_len)
    
    '''
    print("-----���ȴ���seq_len-----")
    txt = text[0]
    print("#text#")
    print(txt)
    print("#encode#" )
    code = T.trim(T.encode(T.tokenize(txt)), seq_len)
    print(code)
    print("#decode#" )
    T.decode(code)
    print("-----����С��seq_len-----")
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