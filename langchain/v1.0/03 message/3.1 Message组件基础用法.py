#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2026/6/8 
@Author : wzy
@File   : 3.1 Message组件基础用法
"""
from datetime import datetime

import dotenv
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage, SystemMessage
from langchain.tools import tool

dotenv.load_dotenv()


# 1.定义工具及对应map
@tool
def get_current_time():
    """获取当前时间"""
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


tools_map = {
    "get_current_time": get_current_time
}

# 2.创建model对象
model = init_chat_model(
    "deepseek-v4-flash"
)

# 3.定义消息列表
human_message = HumanMessage("你好，你是谁？现在什么时间？")
system_message = SystemMessage("你是一个知识问答机器人，你叫老K")
message_list = [human_message, system_message]

# 4.绑定工具
bind_tool_model = model.bind_tools([get_current_time])

# 5.调用LLM模型
ai_message = bind_tool_model.invoke(message_list)
message_list.append(ai_message)

# 6.判断是否有函数调用
if ai_message.tool_calls:
    tool_message = tools_map.get((ai_message.tool_calls[0].get("name"))).invoke(ai_message.tool_calls[0])
    # 7.将工具调用结果ToolMessage添加到消息列表
    message_list.append(tool_message)

# 7.再次调用model
ai_message = bind_tool_model.invoke(message_list)

print(ai_message.content)
