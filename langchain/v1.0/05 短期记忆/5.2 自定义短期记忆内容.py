#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2026/6/11 
@Author : wzy
@File   : 5.2 自定义短期记忆内容
"""
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain.agents import AgentState
from langgraph.checkpoint.memory import InMemorySaver

import dotenv

dotenv.load_dotenv()


# 1.定义短期记忆内容
class CustomState(AgentState):
    username: str


# 2.定义Agent
checkpointer = InMemorySaver()
agent = create_agent(model="deepseek-v4-flash",
                     state_schema=CustomState,
                     checkpointer=checkpointer)

# 3.调用Agent
state = agent.invoke({"messages": [HumanMessage("1+1等于几")], "username": "大志说编程"},
                     config={"configurable": {"thread_id": "1000"}},
                     )

print(state.get("username"))


