#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2026/6/10 
@Author : wzy
@File   : 2.10 直接返回工具执行结果
"""
import dotenv
from langchain.tools import tool
from langchain.agents import create_agent
from langchain.messages import HumanMessage

dotenv.load_dotenv()


# 1.定义工具
@tool("search_weather", description="根据城市名称查询天气信息", return_direct=True)
def search_weather(city: str):
    return {
        "city": city,
        "weather": "晴，气温30C°~35C°"
    }


# 2.创建Agent
agent = create_agent(model="deepseek-v4-flash",
                     system_prompt="你是一个天气查询助手",
                     tools=[search_weather])

# 3.调用Agent
state = agent.invoke({"messages": [HumanMessage("查询杭州天气")]})

# 4.输出结果
print(type(state.get("messages")[-1]))
print(state.get("messages")[-1].content)