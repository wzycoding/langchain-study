#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2026/6/9 
@Author : wzy
@File   : 2.5 获取上下文context
"""
import uuid
from dataclasses import dataclass

import dotenv
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain.tools import tool, ToolRuntime

dotenv.load_dotenv()


# 1.定义用户上下文对象
@dataclass
class UserContext:
    user_id: str


# 2.定义工具
@tool
def get_user_info(runtime: ToolRuntime[UserContext]):
    """获取当前用户信息"""
    # 忽略查询数据库具体操作...
    return f"用户id：{runtime.context.user_id}, 用户名：大志"


# 3.创建Agent
agent = create_agent(model="deepseek-v4-flash",
                     system_prompt="你是一个专门为程序员工作的AI助手",
                     context_schema=UserContext,
                     tools=[get_user_info])

# 4.调用Agent
state = agent.invoke(
    {"messages": [HumanMessage("获取当前用户信息")]},
    context=UserContext(user_id="123"),
    config={"configurable": {"thread_id": str(uuid.uuid4())}}, )

# 5.输出结果
print(state.get("messages")[-1].content)
