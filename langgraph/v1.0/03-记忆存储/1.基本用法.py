#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2025/12/22 
@Author : wzy
@File   : 1.基本用法
"""
import uuid

from langgraph.store.memory import InMemoryStore

# 1.创建InMemoryStore对象
in_memory_store = InMemoryStore()

# 2.向InMemoryStore对象中添加数据
user_id = "1"
namespace = ("history_messages", user_id)
memory_id_1 = str(uuid.uuid4())
memory_id_2 = str(uuid.uuid4())
in_memory_store.put(namespace, memory_id_1, {"role": "human", "content": "你好,我是大志，你是？"})
in_memory_store.put(namespace, memory_id_2, {"role": "ai", "content": "你好，我是OpenAI开发的聊天助手ChatGPT"})

# 3.获取数据通过命名空间和唯一标识
memory_item = in_memory_store.get(namespace, memory_id_1)
print("============get方法获取记忆数据=============")
print(memory_item)

# 4.数据检索
memory_items = in_memory_store.search(namespace)
print("============search方法检索记忆数据列表=============")
print(memory_items)
