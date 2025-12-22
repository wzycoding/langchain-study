#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2025/12/3 
@Author : wzy
@File   : 2.获取图的状态数据
"""

import operator
from typing import TypedDict, Annotated

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.constants import END, START
from langgraph.graph import StateGraph


# 1.定义State
class State(TypedDict):
    result: Annotated[list[str], operator.add]


# 2.定义a节点
def a_node(state: State):
    """调用a节点"""
    print("执行a_node节点")
    return {"result": ["你好，我是a节点"]}


# 3.定义b节点
def b_node(state: State):
    """调用b节点"""
    print("执行b_node节点")
    return {"result": ["你好，我是b节点"]}


# 4.构建编译图
graph = StateGraph(State)

# 5.添加节点、边
graph.add_node("a_node", a_node)
graph.add_node("b_node", b_node)

graph.add_edge(START, "a_node")
graph.add_edge("a_node", "b_node")
graph.add_edge("b_node", END)

# 6.编译并运行图，并指定检查点管理器
checkpointer = InMemorySaver()
agent = graph.compile(checkpointer=checkpointer)

# 7.调用图传入线程id
config = {"configurable": {"thread_id": "1"}}
state = agent.invoke({"result": []}, config)

# 8.获取检查点信息
print("==============获取最新的检查点===============")
latest_state = agent.get_state(config)
print(latest_state)

history_states = agent.get_state_history(config)
print("==============获取历史检查点===============")
for state in history_states:
    print(state)
