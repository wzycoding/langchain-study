#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2025/7/22 
@Author : wzy
@File   : 1.StrOutputParser输出解析器
"""

import dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

# 读取env配置
dotenv.load_dotenv()

# 1.构建提示词
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个资深文学家"),
    ("human", "请简短赏析{name}这首诗，并给出评价")
])

# 2.创建模型
llm = ChatOpenAI()

# 3.创建字符串输出解析器
parser = StrOutputParser()

# 4.构建链式调用
chain = prompt | llm | parser

# 5.执行链式调用
result = chain.invoke({"name": "静夜思"})
print(f"输出类型: {type(result)}")
print(f"输出内容: {result}")