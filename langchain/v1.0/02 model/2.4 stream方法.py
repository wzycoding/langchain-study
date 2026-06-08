#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2026/6/7 
@Author : wzy
@File   : 2.4 stream方法
"""
import dotenv
from langchain.chat_models import init_chat_model

dotenv.load_dotenv()

# 1.创建model对象
model = init_chat_model(
    model="deepseek-v4-flash"
)

result = None

# 2.调用大模型，返回AIMessage
for chunk in model.stream("请你简要介绍一下什么是LangChain框架"):
    print(chunk.text, end="", flush=True)
    print("\n")

    if result is None:
        result = chunk
    else:
        result += chunk

print("\n")
print("--------------------最终完整输出结果----------------------")
print(result.content)
