#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2025/7/24 
@Author : wzy
@File   : 3.RunnableBranch用法
"""
import dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableBranch
from langchain_openai import ChatOpenAI

# 读取env配置
dotenv.load_dotenv()


def judge_language(inputs):
    """判断语言种类"""
    query = inputs["query"]
    if "日语" in query:
        return "japanese"
    elif "韩语" in query:
        return "korean"
    else:
        return "english"


# 1.构建提示词
english_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个英语翻译专家，你叫小英"),
    ("human", "{query}")
])

japanese_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个日语翻译专家，你叫小日"),
    ("human", "{query}")
])

korean_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个韩语翻译专家，你叫小韩"),
    ("human", "{query}")
])

# 2.创建模型
llm = ChatOpenAI()
# 3.创建字符串输出解析器
parser = StrOutputParser()

# 4.构建链分支结构，默认分支为英语
chain = RunnableBranch(
    (lambda x: judge_language(x) == "japanese", japanese_prompt | llm | parser),
    (lambda x: judge_language(x) == "korean", korean_prompt | llm | parser),
    (english_prompt | llm | parser)
)

# 5.执行链
print(f"输出结果：{chain.invoke({'query': '请你用韩语翻译这句话：“我爱你”。并且告诉我你叫什么'})}")
