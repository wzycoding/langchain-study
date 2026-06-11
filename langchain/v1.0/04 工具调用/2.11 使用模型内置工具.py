#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2026/6/10 
@Author : wzy
@File   : 2.11 使用模型内置工具
"""
import dotenv
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain_qwq.chat_models import ChatQwen

dotenv.load_dotenv()

# 1.创建model
llm = ChatQwen(
    model="qwen3.7-max",
    extra_body={
        "enable_search": True,
        "web_extractor": True,
    }
)

# 2.创建Agent
agent = create_agent(model=llm)

# 3.调用Agent
state = agent.invoke({"messages": [HumanMessage("获取今日AI新闻")]})

# 4.输出结果
print(state.get("messages")[-1].content)
