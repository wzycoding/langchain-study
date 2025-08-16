#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2025/8/14 
@Author : wzy
@File   : 1.使用VectorStore作为检索器
"""
import dotenv
import weaviate
from langchain_openai import OpenAIEmbeddings
from langchain_weaviate import WeaviateVectorStore

# 读取env配置
dotenv.load_dotenv()

# 1.创建Weaviate客户端
client = weaviate.connect_to_local(
    host="localhost",
    port=8080,
    grpc_port=50051,
)

# 2.创建文本嵌入模型
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# 3.创建Weaviate向量数据库
vector_store = WeaviateVectorStore(
    client=client,
    text_key="text_key",
    embedding=embeddings,
    index_name="Database"
)

# 4.创建检索器，进行数据检索
retriever = vector_store.as_retriever()
documents = retriever.invoke("介绍一下光明科技公司副总经理的情况。")

for document in documents:
    print(document.page_content)
    print(document.metadata)
    print("=================================")
