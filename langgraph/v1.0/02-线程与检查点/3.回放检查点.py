#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2025/12/3 
@Author : wzy
@File   : 3.回放检查点
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
print("================图执行结束=================")

# 8.获取历史图状态信息
history_states = list(agent.get_state_history(config))
target_checkpoint_index = 1
target_state = history_states[target_checkpoint_index]

# 9.回放检查点
target_checkpoint_id = target_state.config["configurable"]["checkpoint_id"]
replay_config = {"configurable": {"thread_id": "1", "checkpoint_id": target_checkpoint_id}}
replay_state = agent.invoke(None, replay_config)

print("================回放检查点结果=================")
print(replay_state["result"])
