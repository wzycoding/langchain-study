#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2026/7/3 
@Author : wzy
@File   : 结构化输出
"""
import dotenv

dotenv.load_dotenv()
from langchain.agents import create_agent
from pydantic import BaseModel, Field


class UserInfo(BaseModel):
    name: str = Field(description="用户姓名")
    age: int = Field(description="用户年龄")
    tags: list[str] = Field(description="用户标签")


agent = create_agent(
    model="gpt-5.5",
    tools=[],
    response_format=UserInfo,
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "张三今年18岁，喜欢篮球"}]
})

user_info = result["structured_response"]

print(user_info)
