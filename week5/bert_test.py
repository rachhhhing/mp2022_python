from transformers import BertTokenizer, BertModel
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

bert_name = 'bert-base-chinese'
tokenizer = BertTokenizer.from_pretrained(bert_name)
bert_model = BertModel.from_pretrained(bert_name)
sbert_model = SentenceTransformer(bert_name)

with open('week5/clean_text.txt','r',encoding='utf-8') as f:
        data = f.read().splitlines()[:100]
        data = list(filter(None, data))           #去除空值

#编码展示
'''
input_ids = tokenizer.encode(
                        text = data[1],
                        text_pair = data[4],      # 可以编码一个/两个句子
                        truncation=True,          # 当句子长度大于max_length时截断
                        padding='max_length',     # 补pad到max_length长度
                        add_special_tokens=True,  # 添加special tokens,也就是CLS和SEP
                        max_length=30,            # 设定最大文本长度
                        return_tensors=None       # 可取值tf,pt,np,默认为返回list
                   )

print('---text---\n', data[1])
print('---text_pair---\n ', data[4])
print('---input_ids---\n', input_ids)
print('---decode---\n', tokenizer.decode(input_ids))
'''

#生成句子向量展示
'''
tokens = tokenizer.encode_plus(text=data[1], return_tensors='pt')
sen_vec = bert_model(**tokens)
print(sen_vec)
'''

#查找相似文本展示-简单版
'''
sentence_embeddings = sbert_model.encode(data)
#计算余弦相似度
comp_sim = cosine_similarity([sentence_embeddings[1]],sentence_embeddings[2:])[0].tolist()
print("---余弦相似度---\n", comp_sim)
sim_max = max(comp_sim)
index = comp_sim.index(sim_max)
print("---原文本---\n", data[1])
print("---最相似文本---\n", data[2+index])
'''