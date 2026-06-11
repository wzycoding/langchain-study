#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2026/6/11 
@Author : wzy
@File   : 5.1 短期记忆基础用法
"""
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver

import dotenv
dotenv.load_dotenv()

# 1.定义Agent
checkpointer = InMemorySaver()
agent = create_agent(model="deepseek-v4-flash",
                     checkpointer=checkpointer)

# 2.第一次调用Agent
first_human_message = HumanMessage("你好，我是大志，你是？")
state = agent.invoke({"messages": [first_human_message]},
                     config={"configurable": {"thread_id": "1000"}},
                     )
first_content = state.get("messages")[-1].content
print(f"Human：{first_human_message.content}")
print(f"AI:{first_content}")
print("--------------------------------------------")

# 3.第二次调用Agent
second_human_message = HumanMessage("你还记得我是谁吗？")
state = agent.invoke({"messages": ["你还记得我是谁吗？"]},
                     config={"configurable": {"thread_id": "1000"}},
                     )
second_content = state.get("messages")[-1].content
print(f"Human：{second_human_message.content}")
print(f"AI:{second_content}")
