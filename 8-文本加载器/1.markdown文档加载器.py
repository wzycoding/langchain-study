#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2025/8/3 
@Author : wzy
@File   : 1.markdown文档加载器
"""
from langchain_community.document_loaders import UnstructuredMarkdownLoader

# 1.创建文档加载器，并指定路径
document_load = UnstructuredMarkdownLoader(file_path="LangChain框架入门09：什么是RAG？.md",
                                           mode="elements")

# 2.加载文档
documents = document_load.load()

# 3.打印文档内容
print(f"文档数量：{len(documents)}")
for document in documents:
    print(f"文档内容：{document.page_content}")
    print(f"文档元数据：{document.metadata}")
