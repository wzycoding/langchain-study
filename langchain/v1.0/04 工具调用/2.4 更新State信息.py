#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2026/6/9 
@Author : wzy
@File   : 2.4 更新State信息
"""
from datetime import datetime

import dotenv
from langchain.agents import create_agent, AgentState
from langchain.messages import HumanMessage, ToolMessage
from langchain.tools import tool, ToolRuntime
from langgraph.types import Command

dotenv.load_dotenv()


# 1.定义State
class CustomState(AgentState):
    last_search_weather_time: str


# 2.定义工具
@tool
def search_weather(runtime: ToolRuntime, city: str):
    """查询今日天气"""
    return Command(
        update={
            "messages": [
                ToolMessage(
                    content=f"今日{city}天气晴，东风4级，体感舒适",
                    tool_call_id=runtime.tool_call_id,
                )
            ],
            "last_search_weather_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        },
    )


# 3.创建Agent
agent = create_agent(model="deepseek-v4-flash",
                     system_prompt="你是一个专门为程序员工作的AI助手",
                     tools=[search_weather],
                     state_schema=CustomState, )

# 4.调用Agent
state = agent.invoke({
    "messages": [
        HumanMessage("今天杭州天气")
    ],
    "last_search_weather_time": None
})

# 5.输出结果
print(state.get("last_search_weather_time"))
