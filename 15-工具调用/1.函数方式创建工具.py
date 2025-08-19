#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2025/8/19 
@Author : wzy
@File   : 1.函数方式创建工具
"""
from langchain_core.tools import tool
from pydantic.v1 import Field, BaseModel


class AddNumberInput(BaseModel):
    """加法工具入参"""
    num1: int = Field(description="第一个数")
    num2: int = Field(description="第二个数")


@tool("add-tool", args_schema=AddNumberInput, return_direct=True)
def add(num1: int, num2: int):
    """两数相加"""
    return num1 + num2


print(f"工具名称：{add.name}")
print(f"工具描述：{add.description}")
print(f"工具参数：{add.args}")
print(f"是否直接返回：{add.return_direct}")

print("1+1=" + str(add.invoke({"num1": 1, "num2": 1})))
