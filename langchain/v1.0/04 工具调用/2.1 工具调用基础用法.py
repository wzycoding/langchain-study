#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2026/6/7 
@Author : wzy
@File   : 2.1 工具调用
"""
import dotenv
from langchain.agents import create_agent
from langchain.tools import tool

dotenv.load_dotenv()


@tool
def search_weather(city: str):
    """查询今日天气"""
    return f"今日{city}天气晴，东风4级，体感舒适"


agent = create_agent("openai:gpt-4o-mini", tools=[search_weather])
result = agent.invoke({"messages": [{"role": "user", "content": "今天杭州天气如何？"}]})
print(result["messages"][-1].content_blocks)
