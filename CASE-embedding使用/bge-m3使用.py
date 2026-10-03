#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os

# 获取脚本所在目录，模型缓存到脚本下的 models 目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_CACHE_DIR = os.path.join(SCRIPT_DIR, "models")

#模型下载
from modelscope import snapshot_download
model_dir = snapshot_download('BAAI/bge-m3', cache_dir=MODEL_CACHE_DIR)


# In[1]:


from FlagEmbedding import BGEM3FlagModel

model = BGEM3FlagModel(model_dir,
                       use_fp16=True) # Setting use_fp16 to True speeds up computation with a slight performance degradation

sentences_1 = ["What is BGE M3?", "Defination of BM25"]
sentences_2 = ["BGE M3 is an embedding model supporting dense retrieval, lexical matching and multi-vector interaction.", 
               "BM25 is a bag-of-words retrieval function that ranks a set of documents based on the query terms appearing in each document"]

embeddings_1 = model.encode(sentences_1, 
                            batch_size=12, 
                            max_length=8192, # If you don't need such a long length, you can set a smaller value to speed up the encoding process.
                            )['dense_vecs']
embeddings_2 = model.encode(sentences_2)['dense_vecs']
similarity = embeddings_1 @ embeddings_2.T
print(similarity)
# [[0.6265, 0.3477], [0.3499, 0.678 ]]

