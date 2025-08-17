#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2025/8/17 
@Author : wzy
@File   : 1.RAG数据准备
"""
import dotenv
import weaviate
from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_weaviate import WeaviateVectorStore

# 读取env配置
dotenv.load_dotenv()

# 1.文档加载
document_load = TextLoader(file_path="商品信息.md")
documents = document_load.load()

# 2.文档分割
text_splitter = RecursiveCharacterTextSplitter(chunk_size=800,
                                               chunk_overlap=100,
                                               length_function=len,
                                               )
documents = text_splitter.split_documents(documents)

print(f"文档数量：{len(documents)}")
for document in documents:
    print(f"文档片段大小：{len(document.page_content)}")
    print("=====================================")

# 3.文本嵌入
client = weaviate.connect_to_local(
    host="localhost",
    port=8080,
    grpc_port=50051,
)

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# 4.向量数据存储
vector_store = WeaviateVectorStore(
    client=client,
    text_key="text_key",
    embedding=embeddings,
    index_name="Product")

vector_store.add_documents(documents)
