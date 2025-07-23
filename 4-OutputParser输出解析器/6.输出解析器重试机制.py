#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2025/7/23 
@Author : wzy
@File   : 6.输出解析器重试机制
"""

# !/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2025/7/23 
@Author : wzy
@File   : 5.输出解析器重试机制
"""
import dotenv
from langchain_openai import ChatOpenAI
from langchain.output_parsers import RetryOutputParser
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate

# 读取env配置
dotenv.load_dotenv()


# 定义输出的对象结构
class Poetry(BaseModel):
    name: str = Field(description="古诗名字")
    content: str = Field(description="古诗内容")
    author: str = Field(description="古诗作者")


# 1.定义提示模板
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个资深文学家"),
    ("human", "请你输出题目为：{name}这首诗的内容\n{format_instructions}")
])

llm4o = ChatOpenAI(model="gpt-4o")
# 2.构建输出解析器
base_parser = JsonOutputParser(pydantic_object=Poetry)
retry_parser = RetryOutputParser.from_llm(parser=base_parser, llm=llm4o)

# 3.生成prompt_value
prompt_value = prompt.invoke({"name": "登鹳雀楼", "format_instructions": base_parser.get_format_instructions()})

# 4.模拟错误的输出
error_str = "{'content': '白日依山尽，黄河入海流。欲穷千里目，更上一层楼。', 'author': '王之涣'}"
# 5.对比重试前后结果
print(f"重试前的内容:{error_str}")
print(f"重试后的内容:{retry_parser.parse_with_prompt(error_str, prompt_value)}")
