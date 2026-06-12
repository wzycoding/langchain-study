#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2026/6/12
@Author : wzy
@File   : 6.1 在工具中获取长期记忆
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


# 3.定义工具信息
@tool
def get_user_info(runtime: ToolRuntime[Context]) -> str:
    """获取用户信息"""
    user_id = runtime.context.user_id

    user_info = runtime.store.get(("users",), user_id)

    if not user_info:
        return "未找到该用户信息"

    return f"""
            用户信息如下：
            {user_info.value}
            """


# 4.创建agent
agent: Runnable = create_agent(
    model="deepseek-v4-flash",
    tools=[get_user_info],
    store=store,
    context_schema=Context,
)

# 5.调用Agent
result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "帮我查一下这个用户的信息，并简单介绍一下他"
            }
        ]
    },
    context=Context(user_id="user_001"),
)

print(result["messages"][-1].content)
