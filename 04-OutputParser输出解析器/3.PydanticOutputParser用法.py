#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2025/7/22 
@Author : wzy
@File   : PydanticOutputParser
"""
import dotenv
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field, validator
from langchain_openai import ChatOpenAI

# 读取env配置
dotenv.load_dotenv()

# 诗人信息模型
class Poetry(BaseModel):
    name: str = Field(description="古诗名字")
    content: str = Field(description="古诗内容")
    author: str = Field(description="古诗作者")


# 诗歌信息模型
class Poet(BaseModel):
    name: str = Field(description="诗人姓名")
    age: int = Field(description="诗人年龄")
    sex: int = Field(description="性别，0女，1男")
    poetries: list[Poetry] = Field(description="诗歌信息列表")

    # 数据验证器
    @validator('poetries')
    def validate_priority(cls, value):
        if len(value) < 1 :
            raise ValueError('诗歌列表必须大于等于1')
        return value

    @validator('age')
    def validate_hours(cls, value):
        if value <= 0:
            raise ValueError('年龄必须大于0')
        return value


# 1.构建提示词
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个管理中国古代诗人信息的专家"),
    ("human", "请你介绍一下{name}这位诗人的情况\n{format_instructions}")
])

# 2.构建llm
llm = ChatOpenAI(model="gpt-4o")

# 3.构建输出解析器
parser = PydanticOutputParser(pydantic_object=Poet)

# 4.构建链式调用
chain = prompt | llm | parser

# 5.执行链式调用
result = chain.invoke({"name": "李白", "format_instructions": parser.get_format_instructions()})
print(f"输出类型: {type(result)}")
print(f"输出内容: {result}")
