#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2025/7/16 
@Author : wzy
@File   : 1.PromptTemplate用法
"""
from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate.from_template("你是一个专业的律师，请你回答我提出的法律问题，并给出法律条文依据，我的问题是：{question}")
prompt_value = prompt.invoke({"question": "婚姻法是在哪一年颁布的？"})
print(prompt_value)