#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2025/8/5 
@Author : wzy
@File   : 3.MarkdownHeaderTextSplitter用法
"""
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter

# 1.文档加载
loader = TextLoader(file_path="李白.md")
documents = loader.load()
document_text = documents[0].page_content

# 2.定义文本分割器，设置指定要分割的标题
headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2")
]
headers_text_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)

# 3.按标题分割文档
headers_splitter_documents = headers_text_splitter.split_text(document_text)

print(f"按标题分割文档数量：{len(headers_splitter_documents)}")
for splitter_document in headers_splitter_documents:
    print(f"按标题分割文档片段大小：{len(splitter_document.page_content)}, 文档元数据：{splitter_document.metadata}")

# 4.定义递归文本分割器
text_splitter = RecursiveCharacterTextSplitter(chunk_size=100,
                                               chunk_overlap=30,
                                               length_function=len
                                               )

# 5.递归分割文本
recursive_documents = text_splitter.split_documents(headers_splitter_documents)
print(f"第二次递归文本分割文档数量：{len(recursive_documents)}")
for recursive_document in recursive_documents:
    print(
        f"第二次递归文本分割文档片段大小：{len(recursive_document.page_content)}, 文档元数据：{recursive_document.metadata}")
