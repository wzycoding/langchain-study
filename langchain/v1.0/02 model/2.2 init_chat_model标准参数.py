#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2026/6/7 
@Author : wzy
@File   : 2.2 init_chat_model标准参数
"""
import dotenv
from langchain.chat_models import init_chat_model

dotenv.load_dotenv()

# 1.创建model对象
model = init_chat_model(
    model="deepseek-v4-flash",
    temperature=0,  # 温度为0
    max_tokens=500,  # 最大输出token为500
    max_retries=3,  # 服务端错误最大重试次数为3次
    timeout=60  # 模型响应超时时间为60s
)

# 2.调用大模型，返回AIMessage
print(model.invoke("你好，你是？"))
