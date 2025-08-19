#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2025/8/19 
@Author : wzy
@File   : 4.通过继承BaseTool创建工具
"""
from langchain_core.tools import BaseTool
from pydantic.v1 import BaseModel, Field


class AddNumberInput(BaseModel):
    """加法工具入参"""
    num1: int = Field(description="第一个数")
    num2: int = Field(description="第二个数")


class AddNumberTool(BaseTool):
    """加法工具"""
    name = "add_number_tool"
    description = "两数相加工具"
    args_schema = AddNumberInput

    def _run(self, num1: int, num2: int) -> int:
        return num1 + num2


add_number_tool = AddNumberTool()

print(f"工具名称：{add_number_tool.name}")
print(f"工具描述：{add_number_tool.description}")
print(f"工具参数：{add_number_tool.args}")
print(f"是否直接返回：{add_number_tool.return_direct}")

print("1+1=" + str(add_number_tool.invoke({"num1": 1, "num2": 1})))
