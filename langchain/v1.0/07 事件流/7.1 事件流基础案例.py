#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2026/6/14 
@Author : wzy
@File   : 7.1 事件流基础案例
"""
from langchain.agents import create_agent
import dotenv

dotenv.load_dotenv()

# 1.定义工具
def get_weather(city: str) -> str:
    """查询城市天气"""
    return f"{city}今天晴天，气温28°C~35°C"


agent = create_agent(model="deepseek-v4-flash", tools=[get_weather])

# 使用stream_events获取事件流，version="v3"是固定写法
stream = agent.stream_events(
    {"messages": [{"role": "user", "content": "今天杭州天气"}]},
    version="v3"
)

# 流式输出模型回复
for message in stream.messages:
    for delta in message.text:
        print(delta, end="", flush=True)