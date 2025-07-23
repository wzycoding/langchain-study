#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2025/7/16 
@Author : wzy
@File   : 3.MessagesPlaceholder用法
"""
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, SystemMessagePromptTemplate

# prompt = ChatPromptTemplate.from_messages([
#     MessagesPlaceholder("memory"),
#     SystemMessage("你是一个资深的Python应用开发工程师，请认真回答我提出的Python相关的问题"),
#     ("human", "{question}")
# ])
#
# prompt_value = prompt.invoke({"memory": [HumanMessage("我的名字叫大志，是一名程序员"),
#                                          AIMessage("好的，大志你好")],
#                               "question": "请问我的名字叫什么？"})
# print(prompt_value.to_string())


prompt = ChatPromptTemplate.from_messages([
    ("placeholder", "{memory}"),
    SystemMessage("你是一个资深的Python应用开发工程师，请认真回答我提出的Python相关的问题"),
    ("human", "{question}")
])

prompt_value = prompt.invoke({"memory": [HumanMessage("我的名字叫大志，是一名程序员"),
                                         AIMessage("好的，大志你好")],
                              "question": "请问我的名字叫什么？"})
print(prompt_value.to_string())
