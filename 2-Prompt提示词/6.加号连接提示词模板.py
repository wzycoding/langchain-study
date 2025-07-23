#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2025/7/19 
@Author : wzy
@File   : 6.加号连接提示词模板
"""
from langchain_core.prompts import ChatPromptTemplate

# first_chat_prompt = ChatPromptTemplate.from_messages([
#     ("system", "你是OpenAI开发的大语言模型，下面所有提问你扮演小米雷军的角色，对我的提问进行回答")
# ])
#
# second_chat_prompt = ChatPromptTemplate.from_messages([
#     ("human", "{question}")
# ])
#
# all_chat_prompt = first_chat_prompt + second_chat_prompt
#
# print(all_chat_prompt.invoke({"question": "Are you OK?"}).to_string())

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是OpenAI开发的大语言模型，下面所有提问你扮演小米雷军的角色，对我的提问进行回答")
]) + "{question}"
print(chat_prompt.invoke({"question": "Are you OK?"}).to_string())
