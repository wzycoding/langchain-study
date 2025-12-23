#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2025/12/22 
@Author : wzy
@File   : 1.基本用法
"""
import uuid

import dotenv
from langchain.embeddings import init_embeddings
from langgraph.store.memory import InMemoryStore

dotenv.load_dotenv()

# 1.创建InMemoryStore对象
in_memory_store = InMemoryStore(
    index={
        "embed": init_embeddings("openai:text-embedding-3-small"),  # 文本嵌入函数
        "dims": 1536,  # 向量维度
        "fields": ["content", "$"]  # 要进行文本嵌入的字段
    }
)

# 2.向InMemoryStore对象中添加数据
user_id = "1"
namespace = ("history_messages", user_id)
memory_id_1 = str(uuid.uuid4())
memory_id_2 = str(uuid.uuid4())
in_memory_store.put(namespace, memory_id_1, {"role": "human", "content": "你好,我是大志，你是？"})
in_memory_store.put(namespace, memory_id_2, {"role": "ai", "content": "你好，我是OpenAI开发的聊天助手ChatGPT"})

# 3.语义检索
memory_items = in_memory_store.search(namespace, query="大志", limit=1)
print("============search语义检索=============")
print(memory_items)
