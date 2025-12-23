#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2025/12/23 
@Author : wzy
@File   : 3.在LangGraph中使用Memory Store
"""

import operator
import uuid
from typing import TypedDict, Annotated

import dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import AnyMessage, HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig
from langgraph.constants import END, START
from langgraph.graph import StateGraph
from langgraph.store.base import BaseStore
from langgraph.store.memory import InMemoryStore

dotenv.load_dotenv()

# 1.创建llm
llm = init_chat_model(
    "gpt-4o-mini",
    temperature=0
)


# 2.定义State
class MessagesState(TypedDict):
    # 图运行的消息列表
    messages: Annotated[list[AnyMessage], operator.add]
    chat_history: Annotated[list[dict[str, str]], operator.add]


# 3.定义加载记忆节点
def load_memory_node(
        state: MessagesState,
        config: RunnableConfig,
        store: BaseStore
):
    user_id = config["configurable"]["user_id"]
    namespace = ("chat_history", user_id)

    # 1.检索记忆信息
    memories = store.search(namespace)

    # 2.更新到State
    history_messages = []

    for memory in memories:
        history_messages.append({"role": memory.value["role"], "content": memory.value["content"]})

    return {"chat_history": history_messages}


# 4.定义llm节点
def llm_node(state: MessagesState, config: RunnableConfig, store: BaseStore):
    """调用LLM节点"""
    system_prompt = """你是一个智能助手，根据用户提出的问题认真回复
    当前用户历史记忆如下：{chat_history}
    """
    chat_history_str = ""
    for item in state["chat_history"]:
        chat_history_str += f"{item['role']}: {item['content']}\n"
    system_message = SystemMessage(content=system_prompt.format(chat_history=chat_history_str))

    ai_message = llm.invoke([system_message, *state["messages"]])

    return {"messages": [ai_message]}


# 4.定义存储记忆节点
def save_memory_node(
        state: MessagesState,
        config: RunnableConfig,
        store: BaseStore
):
    user_id = config["configurable"]["user_id"]
    namespace = ("chat_history", user_id)

    # 1.保存AIMessage
    for message in state["messages"]:
        store.put(
            namespace,
            str(uuid.uuid4()),
            {
                "role": message.type,
                "content": message.content
            }
        )

    return {}


# 5.构建图
graph = StateGraph(MessagesState)

graph.add_node("load_memory", load_memory_node)
graph.add_node("llm", llm_node)
graph.add_node("save_memory", save_memory_node)

graph.add_edge(START, "load_memory")
graph.add_edge("load_memory", "llm")
graph.add_edge("llm", "save_memory")
graph.add_edge("save_memory", END)

# 6.编译并运行图
in_memory_store = InMemoryStore()
agent = graph.compile(store=in_memory_store)

config = {"configurable": {"user_id": "1"}}
state = agent.invoke({"messages": [HumanMessage(content="你好，我是大志你是？")]}, config)

print("================================== 第一次对话 ==================================")
for message in state["messages"]:
    message.pretty_print()

print("================================== 第二次对话 ==================================")
state = agent.invoke({"messages": [HumanMessage(content="你知道我是谁吗？")]}, config)
for message in state["messages"]:
    message.pretty_print()
