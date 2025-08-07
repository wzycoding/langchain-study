#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2025/8/7 
@Author : wzy
@File   : 2.CacheBackedEmbeddings用法
"""
import time

import dotenv
from langchain.embeddings import CacheBackedEmbeddings
from langchain.storage import LocalFileStore
from langchain_openai import OpenAIEmbeddings

dotenv.load_dotenv()

# 1.创建进行文本嵌入的embeddings对象
underlying_embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# 2.创建CacheBackedEmbeddings对象
cache_embeddings = CacheBackedEmbeddings.from_bytes_store(underlying_embeddings=underlying_embeddings,
                                                          document_embedding_cache=LocalFileStore("./document_cache/"),
                                                          namespace=underlying_embeddings.model,
                                                          query_embedding_cache=LocalFileStore("./query_cache/"))

texts = [
    "北宋著名文学家、书法家、画家，历史治水名人。与父苏洵、弟苏辙三人并称“三苏”。苏轼是北宋中期文坛领袖，在诗、词、散文、书、画等方面取得很高成就。",
    "苏轼，（1037年1月8日-1101年8月24日）字子瞻、和仲，号铁冠道人、东坡居士，世称苏东坡、苏仙，汉族，眉州眉山（四川省眉山市）人",
    "与辛弃疾同是豪放派代表，并称“苏辛”；散文著述宏富，豪放自如，与欧阳修并称“欧苏”，为“唐宋八大家”之一。苏轼善书，“宋四家”之一；擅长文人画，尤擅墨竹、怪石、枯木等。与韩愈、柳宗元和欧阳修合称“千古文章四大家”。",
]

# 3.将文本转换为向量
start_time = time.time()
vectors = cache_embeddings.embed_documents(texts)
print(f"文档嵌入执行时间：{time.time() - start_time:.4f} 秒")

# 5.将查询转换为向量
start_time = time.time()
query = "谁是苏东坡？"
query_vector = cache_embeddings.embed_query(query)

# 6.输出查询文本向量
print(f"查询文本嵌入执行时间：{time.time() - start_time:.4f} 秒")
