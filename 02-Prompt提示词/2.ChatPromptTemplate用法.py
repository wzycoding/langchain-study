#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2025/7/16 
@Author : wzy
@File   : ChatPromptTemplate用法
"""
from langchain_core.prompts import ChatPromptTemplate

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个资深的Python应用开发工程师，请认真回答我提出的Python相关的问题，并确保没有错误"),
    ("human", "请写一个Python程序，关于{question}")
])

print(chat_prompt.invoke({"question": "冒泡排序"}))