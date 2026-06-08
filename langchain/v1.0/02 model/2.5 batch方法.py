#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2026/6/7 
@Author : wzy
@File   : 2.5 batch方法
"""
import dotenv
from langchain.chat_models import init_chat_model

dotenv.load_dotenv()

# 1.创建model对象
model = init_chat_model(
    model="deepseek-v4-flash"
)

results = model.batch([
    "你好你是",
    "你是什么模型？",
    "你的上下文窗口多大？"
], config={
    'max_concurrency': 2,  # 限制最多2个并发调用
})

for result in results:
    print(result)
