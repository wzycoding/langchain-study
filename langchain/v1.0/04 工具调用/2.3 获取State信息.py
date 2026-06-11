#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2026/6/9 
@Author : wzy
@File   : 2.3 工具获取State信息
"""
import dotenv
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain.tools import tool, ToolRuntime

dotenv.load_dotenv()


# 1.定义工具
@tool
def search_weather(runtime: ToolRuntime, city: str):
    """查询今日天气"""
    print(runtime.state["messages"])
    return f"今日{city}天气晴，东风4级，体感舒适"


# 2.创建Agent
agent = create_agent(model="deepseek-v4-flash",
                     system_prompt="你是一个专门为程序员工作的AI助手",
                     tools=[search_weather])

# 3.调用Agent
state = agent.invoke({
    "messages": [
        HumanMessage("今天杭州天气")
    ]
})

# 4.输出结果
print(state.get("messages")[-1].content)
