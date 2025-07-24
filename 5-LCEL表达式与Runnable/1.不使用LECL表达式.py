#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2025/7/24 
@Author : wzy
@File   : 1.不使用LECL表达式
"""
import dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

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

# 4.调用模型返回结果
result = parser.invoke(
    llm.invoke(
        prompt.invoke({"name": "江雪"})
    )
)

print(f"输出结果：{result}")
