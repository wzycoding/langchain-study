#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2026/6/9 
@Author : wzy
@File   : 2.3 获取长期记忆信息
"""

import dotenv
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain.tools import tool, ToolRuntime
from langgraph.store.memory import InMemoryStore
from pydantic import BaseModel, Field

dotenv.load_dotenv()


# 1.定义用户信息
class UserInfo(BaseModel):
    """用户信息"""
    id: str = Field(description="用户id")
    name: str = Field(description="用户名")
    sex: str = Field(description="性别")


# 2.定义工具信息
@tool
def get_user_info(runtime: ToolRuntime, user_id: str):
    """获取用户信息"""
    return runtime.store.get(("users",), user_id)


@tool(args_schema=UserInfo)
def add_user_info(runtime: ToolRuntime, id: str, name: str, sex: str):
    """添加用户信息"""
    return runtime.store.put(("users",), id, UserInfo(id=id, name=name, sex=sex))


store = InMemoryStore()
# 3.创建Agent
agent = create_agent(model="deepseek-v4-flash",
                     system_prompt="你是一个专门为程序员工作的AI助手",
                     tools=[get_user_info, add_user_info],
                     store=store)

# 4.调用Agent
state = agent.invoke({
    "messages": [
        HumanMessage("保存用户信息，用户id：1，用户名：张三，性别：男")
    ]
})

state = agent.invoke({
    "messages": [
        HumanMessage("获取用户id为1的用户信息")
    ]
})

# 5.输出结果
print(state.get("messages")[-1].content)
