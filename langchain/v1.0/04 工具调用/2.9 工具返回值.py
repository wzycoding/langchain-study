#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2026/6/10 
@Author : wzy
@File   : 2.9 工具返回值
"""

import dotenv
from datetime import datetime
from langchain.messages import ToolMessage
from langchain.tools import tool, ToolRuntime
from langgraph.types import Command

dotenv.load_dotenv()


# 1.直接返回字符串的工具
@tool("search_ip_location", description="通过用户提供的ip地址，获取对应地理位置")
def get_ip_location(ip: str) -> str:
    """通过ip地址获取位置信息

    Args:
        ip: 要查询定位的ip地址
    """
    return f"ip地址：{ip}，定位地址：浙江杭州"


# 2.返回对象的工具
@tool("get_user_info", description="根据用户id，获取用户信息")
def get_user_info(user_id: str) -> dict[str, any]:
    return {
        "id": user_id,
        "name": "李四",
        "sex": "女",
        "phone": "131xxxxxxxxx"
    }


# 3.返回Command的工具
@tool("search_weather", description="通过传递的城市信息查询天气")
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
