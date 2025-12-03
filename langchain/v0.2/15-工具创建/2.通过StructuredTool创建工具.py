#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2025/8/19 
@Author : wzy
@File   : 2.通过StructuredTool创建工具
"""
import asyncio

from langchain_core.tools import StructuredTool
from pydantic.v1 import BaseModel, Field


class AddNumberInput(BaseModel):
    """加法工具入参"""
    num1: int = Field(description="第一个数")
    num2: int = Field(description="第二个数")


def add(num1: int, num2: int):
    """两数相加"""
    return num1 + num2


async def async_add(num1: int, num2: int):
    """两数相加"""
    return num1 + num2


add_tool = StructuredTool.from_function(
    func=add,
    coroutine=async_add,
    name="add_tool",
    description="两数相加",
    args_schema=AddNumberInput,
    return_direct=True,
)

print(f"工具名称：{add_tool.name}")
print(f"工具描述：{add_tool.description}")
print(f"工具参数：{add_tool.args}")
print(f"是否直接返回：{add_tool.return_direct}")

# 同步调用工具
print("1+1=" + str(add_tool.invoke({"num1": 1, "num2": 1})))


# 异步调用工具
async def async_main():
    result = await add_tool.ainvoke({"num1": 2, "num2": 5})
    print("2+5=" + str(result))


asyncio.run(async_main())
