#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2025/8/4 
@Author : wzy
@File   : 2.RecursiveCharacterTextSplitter分割文档对象
"""
from langchain_community.document_loaders import UnstructuredFileLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 1.创建文档加载器，进行文档加载
loader = UnstructuredFileLoader(file_path="李白.txt")
documents = loader.load()

# 2.定义递归文本分割器
text_splitter = RecursiveCharacterTextSplitter(chunk_size=100,
                                               chunk_overlap=30,
                                               length_function=len,
                                               separators=["。", "?", "\n\n", "\n", " ", ""]
                                               )

# 3.分割文本
splitter_documents = text_splitter.split_documents(documents)

print(f"分割文档数量：{len(splitter_documents)}")
for splitter_document in splitter_documents:
    print(f"文档片段大小：{len(splitter_document.page_content)}, 文档元数据：{splitter_document.metadata}")
