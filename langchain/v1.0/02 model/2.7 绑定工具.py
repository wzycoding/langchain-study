#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2026/6/8 
@Author : wzy
@File   : 2.7 绑定工具
"""
import dotenv
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage
from langchain.tools import tool

dotenv.load_dotenv()


# 1、定义工具
@tool
def get_today_ai_news() -> str:
    """获取今天最新的AI资讯"""
    return (
        "1. Agent成为AI核心方向\n"
        "2. GPT-5.5强化推理与编程\n"
        "3. Claude新版本提升代码能力\n"
        "4. Gemini升级多模态能力\n"
        "5. AI正进入操作系统层"
    )


@tool
def search_weather(city: str):
    """查询今日天气"""
    return f"今日{city}天气晴，东风4级，体感舒适"


# 2、构建工具名->工具函数的映射
tools_map = {
    "get_today_ai_news": get_today_ai_news,
    "search_weather": search_weather
}

# 3.创建model对象
model = init_chat_model(
    model="deepseek-v4-flash"
)

# 4.绑定工具
bind_tools_model = model.bind_tools([get_today_ai_news, search_weather])
messages = [
    HumanMessage("获取今日最新AI资讯")
]

# 5.执行循环
while True:
    ai_message = bind_tools_model.invoke(messages)
    messages.append(ai_message)
    if not ai_message.tool_calls:
        break

    for tool_call in ai_message.tool_calls:
        tool_message = tools_map.get(tool_call.get("name")).invoke(tool_call)
        # 6、添加工具消息到消息列表
        messages.append(tool_message)

# 7.输出结果
print(f"最终结果：{messages[-1].content}")
