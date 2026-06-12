#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2026/6/12 
@Author : wzy
@File   : 6.2 在工具中写入长期记忆
"""
from dataclasses import dataclass

from langchain.agents import create_agent
from langchain.tools import ToolRuntime, tool
from langchain_core.runnables import Runnable
from langgraph.store.memory import InMemoryStore
import dotenv

dotenv.load_dotenv()


# 1.定义用户上下文
@dataclass
class Context:
    user_id: str


# 2.定义store并添加数据
store = InMemoryStore()

store.put(
    ("users",),
    "user_001",
    {
        "name": "大志",
        "language": "中文",
        "job": "Java高级开发工程师",
        "interest": ["LangChain", "AI Agent", "公众号写作"]
    },
)

# 3.定义工具：写入长期记忆信息
@tool
def update_user_memory(runtime: ToolRuntime[Context], info: str) -> str:
    """写入用户长期记忆"""

    user_id = runtime.context.user_id

    # 1.读取已有记忆
    old = runtime.store.get(("users",), user_id)

    old_value = old.value if old else {}

    # 2.合并新记忆
    new_memory = {
        **old_value,
        "extra_info": info
    }

    # 3.写入长期记忆
    runtime.store.put(
        ("users",),
        user_id,
        new_memory
    )

    return f"""
            已写入长期记忆：
            {new_memory}
            """


# 4.创建agent
agent: Runnable = create_agent(
    model="deepseek-v4-flash",
    tools=[update_user_memory],
    store=store,
    context_schema=Context,
)


# 5.调用Agent
result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "帮我记住：我最近在学习微服务架构，并且在用 Spring Cloud"
            }
        ]
    },
    context=Context(user_id="user_001"),
)

# 6.获取store内容
print(store.get(("users",), "user_001"))