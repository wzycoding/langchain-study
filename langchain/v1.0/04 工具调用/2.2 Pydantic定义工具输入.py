#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2026/6/9 
@Author : wzy
@File   : 2.2 使用Pydantic定义模型输入
"""

from langchain.tools import tool
from pydantic import BaseModel, Field


class SearchUserInput(BaseModel):
    nickname: str = Field(description="用户名")
    sex: str = Field(description="用户性别")


@tool(args_schema=SearchUserInput)
def get_user_info(nickname: str, sex: str) -> str:
    return f"用户名：{nickname}, 性别：{sex}, 年龄：18, 简介：这个人很懒什么都没有留下"
