#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2026/6/12 
@Author : wzy
@File   : 6.1 在工具中获取长期记忆
"""
from collections.abc import Sequence
from typing import TypedDict

from langchain.messages import HumanMessage
from langchain.agents import create_agent
from langchain.agents.middleware import ModelRequest, after_model
from langgraph.store.base import IndexConfig
from langgraph.store.memory import InMemoryStore
from langchain_openai import OpenAIEmbeddings

import dotenv

dotenv.load_dotenv()

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)


def embed(texts: Sequence[str]) -> list[list[float]]:
    return embeddings.embed_documents(list(texts))


@after_model
def save_long_term_memory(request: ModelRequest):
    memory_store = request.runtime.store
    namespace = request.runtime.context["namespace"]

    messages = request.state["messages"]

    memory_store.put(
        namespace,
        "auto-memory",
        {"text": messages[-1].content}
    )


class Context(TypedDict):
    user_id: str
    namespace: tuple


# 1.定义Agent
store = InMemoryStore(index=IndexConfig(embed=embed, dims=1536))
agent = create_agent(model="deepseek-v4-flash",
                     store=store,
                     context_schema=Context)

agent.invoke({"messages": [HumanMessage()], }, context={
    "user_id": "123",
    "namespace": ("dazhi", "memory")
})

