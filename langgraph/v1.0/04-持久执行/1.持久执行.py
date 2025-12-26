#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2025/12/3 
@Author : wzy
@File   : 1.持久执行
"""

import operator
from typing import TypedDict, Annotated

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.constants import END, START
from langgraph.func import task
from langgraph.graph import StateGraph


# 1.定义State
class State(TypedDict):
    result: Annotated[list[str], operator.add]


# 2.定义写入日志task
@task
def write_log_task():
    # todo: 写入日志
    print("=========写入日志========")
    return


# 3.定义存储日志节点
def save_log_node(state: State):
    """存储日志节点"""
    uuid = write_log_task()
    return


# 4.构建编译图
graph = StateGraph(State)

# 5.添加节点、边
graph.add_node("save_log", save_log_node)

graph.add_edge(START, "save_log")
graph.add_edge("save_log", END)

# 6.编译并运行图，并指定检查点管理器
checkpointer = InMemorySaver()
agent = graph.compile(checkpointer=checkpointer)

# 7.调用图传入线程id
config = {"configurable": {"thread_id": "1"}}
state = agent.invoke({"result": []}, config, durability="sync")
