#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2025/12/3 
@Author : wzy
@File   : 1.第一个LangGraph程序
"""

import operator
from typing import TypedDict, Literal, Annotated

import dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import AnyMessage, ToolMessage, HumanMessage
from langchain_core.tools import tool
from langgraph.constants import END
from langgraph.graph import StateGraph

dotenv.load_dotenv()

# 1.定义llm和工具
llm = init_chat_model(
    "gpt-4o-mini",
    temperature=0
)


@tool
def add_tow_numbers(a: int, b: int) -> int:
    """两个数相加 `a` 和 `b`.

    Args:
        a: 第一个整数
        b: 第二个整数
    """
    return a + b


@tool
def sub_tow_numbers(a: int, b: int) -> int:
    """两个数相减 `a` 和 `b`.

    Args:
        a: 第一个整数
        b: 第二个整数
    """
    return a + b


@tool
def multi_tow_numbers(a: int, b: int) -> int:
    """两个数相乘 `a` 和 `b`.

    Args:
        a: 第一个整数
        b: 第二个整数
    """
    return a * b


@tool
def divide_tow_numbers(a: int, b: int) -> int:
    """两个数相除 `a` 和 `b`.

    Args:
        a: 第一个整数
        b: 第二个整数
    """
    return a / b


# 2.将工具绑定到LLM
tools = [add_tow_numbers, sub_tow_numbers, multi_tow_numbers, divide_tow_numbers]
llm_with_tool = llm.bind_tools(tools)

# 3.生成工具名称->工具对象的映射
tools_by_name = {tool.name: tool for tool in tools}


# 4.定义State
class MessagesState(TypedDict):
    # 图运行的消息列表
    messages: Annotated[list[AnyMessage], operator.add]


# 5.定义llm节点
def llm_node(state: MessagesState):
    """调用LLM节点"""
    ai_message = llm_with_tool.invoke(state["messages"])

    return {"messages": [ai_message]}


# 6.定义工具节点
def tool_node(state: MessagesState):
    """工具调用"""
    tool_messages = []
    for tool_call in state["messages"][-1].tool_calls:
        tool = tools_by_name[tool_call["name"]]
        tool_output = tool.invoke(tool_call["args"])
        tool_messages.append(ToolMessage(
            content=tool_output,
            tool_call_id=tool_call["id"],
            name=tool_call["name"],
        ))
    return {
        "messages": tool_messages
    }


# 7.条件边路由函数
def llm_tool_route(state: MessagesState) -> Literal["tool_node", END]:
    """工具调用和LLM调用的边路由"""
    if state["messages"][-1].tool_calls:
        return "tool"

    return END


# 8.构建编译图
graph = StateGraph(MessagesState)

graph.add_node("llm", llm_node)
graph.add_node("tool", tool_node)

graph.set_entry_point("llm")
graph.add_conditional_edges("llm", llm_tool_route, ["tool", END])
graph.add_edge("tool", "llm")

# 9.编译并运行图
agent = graph.compile()
state = agent.invoke({"messages": [HumanMessage(content="请计算1+1")]})

for message in state["messages"]:
    message.pretty_print()
