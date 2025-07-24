#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2025/7/24 
@Author : wzy
@File   : 4.RunnableLambda用法
"""
import dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_openai import ChatOpenAI

# 读取env配置
dotenv.load_dotenv()


def character_counter(text):
    """统计输出字符个数"""
    return len(text)


# 1.构建提示词
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个资深文学家"),
    ("human", "请以{subject}为主题写一首古诗")
])

# 2.创建模型
llm = ChatOpenAI()
# 3.创建字符串输出解析器
parser = StrOutputParser()

# 4.构建链
chain = prompt | llm | parser | RunnableLambda(character_counter)

# 5.执行链
print(f"输出结果：{chain.invoke({'subject': '大雪'})}")
