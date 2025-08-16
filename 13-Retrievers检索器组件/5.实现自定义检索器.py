#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2025/8/15 
@Author : wzy
@File   : 5.实现自定义检索器
"""
from typing import List

from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever


class KeywordsRetriever(BaseRetriever):
    """自定义检索器"""
    documents: List[Document]
    k: int

    def _get_relevant_documents(self, query: str, *, run_manager: CallbackManagerForRetrieverRun) -> List[Document]:
        # 1.去除kwargs中的k参数
        k = self.k if self.k is not None else 3
        documents_result = []

        # 2.按照空格拆分query，为多个关键词
        query_keywords = query.split(" ")

        # 3.遍历文档，只要文档中包含其中一个关键词，添加到结果中
        for document in self.documents:
            if any(query_keyword in document.page_content for query_keyword in query_keywords):
                documents_result.append(document)

        # 4.返回前k条文档数据
        return documents_result[:k]


# 1.定义文档列表
documents = [
    Document("光明科技公司总部位于北京市朝阳区，是一家专注于人工智能与大数据分析的高新技术企业，现有员工500人。"),
    Document("董事长张三，男，40岁，籍贯黑龙江漠河市，毕业于清北大学，曾在硅谷工作十年，现负责公司战略规划与重大项目决策。"),
    Document("总经理李四，男，38岁，江苏南京人，拥有十五年软件工程经验，主导过多个国家重点科技项目。"),
    Document("副总经理王五，男，35岁，四川成都人，负责公司运营管理与市场拓展。"),
    Document("技术部拥有120名开发人员，主要从事机器学习模型训练、数据挖掘、云计算平台研发等工作。"),
    Document("光明科技公司在2024年获得国家科技进步二等奖，并与多所高校建立产学研合作关系。"),
    Document("公司设有技术部、市场部、运营部和人力资源部，其中技术部是公司的核心部门。"),
    Document("张三不仅担任董事长，还热衷公益事业，曾多次捐助贫困地区教育项目。"),
    Document("总经理李四毕业于上海交通大学计算机系，擅长分布式系统与云架构设计。"),
    Document("副总经理王五在加入光明科技公司前，曾任某知名互联网企业运营总监，具有丰富的企业管理经验。"),
]

# 2.创建检索器
retriever = KeywordsRetriever(documents=documents, k=1)

# 3.检索得到结果
result = retriever.invoke("张三")

# 4.打印检索结果
for document in result:
    print(document.page_content)
    print("===========================")
