#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2025/8/13 
@Author : wzy
@File   : 2.WeaviateVectorStore数据检索
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

# 4、进行数据检索
search_result = vector_store.similarity_search_with_relevance_scores(query="光明公司的董事长是谁？", k=3)

# 5、打印检索结果
for document, score in search_result:
    print(f"文档内容：{document.page_content}")
    print(f"文档元数据信息：{document.metadata}")
    print(f"相关度得分：{score}")
    print("=================================")
