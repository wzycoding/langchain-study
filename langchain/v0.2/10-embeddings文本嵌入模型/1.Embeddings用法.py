#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2025/8/7 
@Author : wzy
@File   : 1.embeddings用法
"""
import dotenv
from langchain_openai import OpenAIEmbeddings

dotenv.load_dotenv()
texts = [
    "北宋著名文学家、书法家、画家，历史治水名人。与父苏洵、弟苏辙三人并称“三苏”。苏轼是北宋中期文坛领袖，在诗、词、散文、书、画等方面取得很高成就。",
    "苏轼，（1037年1月8日-1101年8月24日）字子瞻、和仲，号铁冠道人、东坡居士，世称苏东坡、苏仙，汉族，眉州眉山（四川省眉山市）人",
    "与辛弃疾同是豪放派代表，并称“苏辛”；散文著述宏富，豪放自如，与欧阳修并称“欧苏”，为“唐宋八大家”之一。苏轼善书，“宋四家”之一；擅长文人画，尤擅墨竹、怪石、枯木等。与韩愈、柳宗元和欧阳修合称“千古文章四大家”。",
]

# 1.创建embeddings对象
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# 2.将文本转换为向量
vectors = embeddings.embed_documents(texts)

# 3.输出文档向量
print("文档向量：")
for vector in vectors:
    print(f"{vector}")

print("=================================")

# 4.将查询转换为向量
query = "谁是苏东坡？"
query_vector = embeddings.embed_query(query)

# 5.输出查询文本向量
print("查询文本向量：")
print(query_vector)
