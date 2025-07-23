#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2025/7/20 
@Author : wzy
@File   : 1.ChatModel使用方法
"""
import dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# 读取env配置
dotenv.load_dotenv()

# 1.构建提示词
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个资深的Python开发工程师"),
    ("human", "{question}")
])

# 2.创建模型
llm = ChatOpenAI()

# 3.生成提示词
prompt_value = prompt.invoke({"question": "请你帮我写一个求最大公约数方法"})

# 4.大模型接收promptValue，输出AI消息
aiMessage = llm.invoke(prompt_value)

# 5.打印AI消息和AI消息内容
print(aiMessage.content)
print(aiMessage.type)
print(aiMessage)
