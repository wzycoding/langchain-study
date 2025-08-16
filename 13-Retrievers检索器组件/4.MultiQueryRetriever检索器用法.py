#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2025/8/15 
@Author : wzy
@File   : 4.MultiQueryRetriever检索器用法
"""
import logging

import dotenv
import weaviate
from langchain.retrievers import MultiQueryRetriever
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_weaviate import WeaviateVectorStore

# 日志设置
logging.basicConfig()
logging.getLogger("langchain.retrievers.multi_query").setLevel(logging.INFO)

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

# 4.创建多查询检索器
retriever = vector_store.as_retriever()
retriever_from_llm = MultiQueryRetriever.from_llm(
    retriever=retriever, llm=ChatOpenAI(model="gpt-3.5-turbo"),
    prompt=PromptTemplate(
        input_variables=["question"],
        template="""你是一个 AI 语言模型助手。你的任务是：
        为给定的用户问题生成 3 个不同的版本，以便从向量数据库中检索相关文档。
        通过生成用户问题的多种视角（改写版本），
        你的目标是帮助用户克服基于距离的相似性搜索的某些局限性。
        请将这些改写后的问题用换行符分隔开。原始问题：{question}""")
)

# 5.进行数据检索
documents = retriever_from_llm.invoke("介绍一下董事长信息")

for document in documents:
    print(document.page_content)
    print(document.metadata)
    print("=================================")
