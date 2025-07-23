#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2025/7/22 
@Author : wzy
@File   : 2.JsonOutputParser输出解析器
"""
import dotenv
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI

# 读取env配置
dotenv.load_dotenv()


# 1.定义输出的对象结构
class Poetry(BaseModel):
    name: str = Field(description="古诗名字")
    content: str = Field(description="古诗内容")
    author: str = Field(description="古诗作者")


# 1.构建提示词
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个资深文学家"),
    ("human", "请你输出题目为：{name}这首诗的内容\n{format_instructions}")
])

# 2.构建llm
llm = ChatOpenAI(model="gpt-4o")

# 3.构建输出解析器
parser = JsonOutputParser(pydantic_object=Poetry)

# 4.构建链式调用
chain = prompt | llm | parser

# 5.执行链式调用
result = chain.invoke({"name": "登鹳雀楼", "format_instructions": parser.get_format_instructions()})
print(f"输出类型: {type(result)}")
print(f"输出内容: {result}")