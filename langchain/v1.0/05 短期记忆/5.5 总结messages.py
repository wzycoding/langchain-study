#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2026/6/11 
@Author : wzy
@File   : 5.5 总结messages
"""
from langchain.messages import HumanMessage
from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware
from langchain_core.runnables import RunnableConfig

from langgraph.checkpoint.memory import InMemorySaver

import dotenv

dotenv.load_dotenv()


# 1.定义Agent
checkpointer = InMemorySaver()
agent = create_agent(model="deepseek-v4-flash",
                     system_prompt="你是一个专门为程序员服务的AI助手",
                     middleware=[SummarizationMiddleware(
                         model="deepseek-v4-flash",
                         trigger=("tokens", 100),
                         keep=("messages", 2)
                     )],
                     checkpointer=checkpointer)

# 2.调用Agent
config: RunnableConfig = {"configurable": {"thread_id": "1001"}}

agent.invoke({"messages": [HumanMessage("我是大志你是")]}, config=config)
agent.invoke({"messages": [HumanMessage("1+1等于几？")]}, config=config)
agent.invoke({"messages": [HumanMessage("1+2等于几？")]}, config=config)
agent.invoke({"messages": [HumanMessage("1+3等于几？")]}, config=config)

result = agent.invoke({"messages": [HumanMessage("你知道我是谁吗？")]}, config=config)
print(result.get("messages")[-1].content)
print(result.get("messages"))