#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2025/7/23 
@Author : wzy
@File   : 5.输出解析器重试机制
"""
import dotenv
from langchain_openai import ChatOpenAI
from langchain.output_parsers import OutputFixingParser, RetryOutputParser
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field

# 读取env配置
dotenv.load_dotenv()


# 定义输出的对象结构
class Poetry(BaseModel):
    name: str = Field(description="古诗名字")
    content: str = Field(description="古诗内容")
    author: str = Field(description="古诗作者")


llm4o = ChatOpenAI(model="gpt-4o")
# 1.构建输出解析器
base_parser = JsonOutputParser(pydantic_object=Poetry)
fixing_parser = OutputFixingParser.from_llm(parser=base_parser, llm=llm4o)

# 2.模拟错误的输出
error_str = "{'content': '白日依山尽，黄河入海流。欲穷千里目，更上一层楼。', 'author': '王之涣'}"

# 3.对比修复前后结果
print(f"修复前的内容:{error_str}")
print(f"修复后的内容:{fixing_parser.parse(error_str)}")
