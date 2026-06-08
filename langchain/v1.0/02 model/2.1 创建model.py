#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2026/6/7 
@Author : wzy
@File   : 2.1 创建model
"""
import dotenv
from langchain.chat_models import init_chat_model

dotenv.load_dotenv()

# 1.创建model对象
model = init_chat_model(
    "deepseek-v4-flash"
)

# 2.调用大模型，返回AIMessage
print(model.invoke("你好，你是？"))
