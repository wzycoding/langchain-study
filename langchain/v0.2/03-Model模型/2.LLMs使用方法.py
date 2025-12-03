#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2025/7/20 
@Author : wzy
@File   : 2.LLMs使用方法
"""
import dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI

# 读取env配置
dotenv.load_dotenv()

# 1.构建提示词
prompt = PromptTemplate.from_template("{question}")

# 2.创建模型
llm = OpenAI()

prompt_value = prompt.invoke({"question": "请完整输出悯农这首诗"})

# 3.文本生成模型接受promptValue，并输出结果
print(llm.invoke(prompt_value))