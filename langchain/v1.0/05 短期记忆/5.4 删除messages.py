#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2026/6/11 
@Author : wzy
@File   : 5.4 删除messages
"""
from langchain.messages import HumanMessage
from langchain.messages import RemoveMessage
from langchain.agents import create_agent, AgentState
from langchain.agents.middleware import after_model
from langgraph.runtime import Runtime
from langchain_core.runnables import RunnableConfig
from typing import Any

from langgraph.checkpoint.memory import InMemorySaver

import dotenv

dotenv.load_dotenv()


# 1、定义消息删除中间件
@after_model
def delete_messages(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    messages = state["messages"]
    if len(messages) <= 2:
        return None

    return {
        "messages": [
            RemoveMessage(id=m.id) for m in messages[:2]
        ]
    }


# 2.定义Agent
checkpointer = InMemorySaver()
agent = create_agent(model="deepseek-v4-flash",
                     system_prompt="你是一个专门为程序员服务的AI助手",
                     middleware=[delete_messages],
                     checkpointer=checkpointer)

# 3.调用Agent
config: RunnableConfig = {"configurable": {"thread_id": "1001"}}

agent.invoke({"messages": [HumanMessage("我是大志你是")]}, config=config)
agent.invoke({"messages": [HumanMessage("1+1等于几？")]}, config=config)
result = agent.invoke({"messages": [HumanMessage("你知道我是谁吗？")]}, config=config)
print(result.get("messages")[-1].content)