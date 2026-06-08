#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2026/5/31 
@Author : wzy
@File   : 01 什么是Agent？
"""
from dotenv import load_dotenv

# 加载env配置
load_dotenv()

from langchain.agents import create_agent


# 1.定义工具
def get_today_ai_news() -> str:
    """获取今天最新的AI资讯"""
    return (
        "1. Agent成为AI核心方向\n"
        "2. GPT-5.5强化推理与编程\n"
        "3. Claude新版本提升代码能力\n"
        "4. Gemini升级多模态能力\n"
        "5. AI正进入操作系统层"
    )


# 2.创建Agent
agent = create_agent(model="openai:gpt-5.4",
                     system_prompt="你是一个专门为程序员工作的AI助手",
                     tools=[get_today_ai_news])

# 3.调用Agent
result = agent.invoke({"messages": [{"role": "user", "content": "今天有哪些热门AI资讯？"}]})

# 4.输出结果
print(result["messages"][-1].content_blocks)