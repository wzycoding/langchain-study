#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2026/6/7 
@Author : wzy
@File   : 2.3 model调用方法
"""
import dotenv
from langchain.chat_models import init_chat_model
from langchain.messages import SystemMessage, HumanMessage

dotenv.load_dotenv()

# 1.创建model对象
model = init_chat_model(
    model="deepseek-v4-flash"
)

# 2.调用大模型，返回AIMessage
print("----------------------传递字符串-------------------")
print(model.invoke("你好，你是？").content)
print("----------------------传递消息列表-------------------")
print(model.invoke([
    {"role": "system", "content": "你是一个AI智能助手，你的名字叫flash助手"},
    {"role": "human", "content": "你好你是"},
]).content)
print("----------------------传递消息对象列表-------------------")
print(model.invoke([
    SystemMessage("你是一个AI智能助手，你的名字叫flash助手"),
    HumanMessage("你好你是"),
]).content)
