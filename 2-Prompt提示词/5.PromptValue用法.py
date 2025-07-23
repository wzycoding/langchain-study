#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2025/7/16 
@Author : wzy
@File   : 5.PromptValue用法
"""
from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate.from_template("你是一个专业的律师，请你回答我提出的法律问题，并给出法律条文依据，我的问题是：{question}")
prompt_value = prompt.invoke({"question": "扰乱公共秩序违法吗？"})
print(prompt_value.to_messages())
print("=================")
print(prompt_value.to_string())