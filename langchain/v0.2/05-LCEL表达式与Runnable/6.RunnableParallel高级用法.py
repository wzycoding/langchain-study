#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2025/7/24 
@Author : wzy
@File   : 6.RunnableParallel高级用法
"""
from operator import itemgetter

import dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# 读取env配置
dotenv.load_dotenv()


def retrieval_doc(question):
    """模拟知识库检索"""
    print(f"检索器接收到用户提出问题：{question}")
    return "你是一个愤怒的语文老师，你叫Bob"


# 1.构建提示词
prompt = ChatPromptTemplate.from_messages([
    ("system", "{retrieval_info}"),
    ("human", "{question}")
])

# 2.创建模型
llm = ChatOpenAI()
# 3.创建字符串输出解析器
parser = StrOutputParser()

# 4.构建链
chain = {
            "retrieval_info": lambda x: retrieval_doc(x["question"]),
            "question": itemgetter("question")
        } | prompt | llm | parser

# 5.执行链
print(f"输出结果：{chain.invoke({'question': '你是谁，能否帮我写一首诗？'})}")
