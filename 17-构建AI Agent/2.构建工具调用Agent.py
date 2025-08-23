#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2025/8/23 
@Author : wzy
@File   : 2.构建工具调用Agent
"""
import os

import dotenv
import requests
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_message_histories import FileChatMessageHistory
from langchain_community.tools import GoogleSerperRun
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import BaseTool
from langchain_openai import ChatOpenAI
from pydantic.v1 import BaseModel, Field

# 读取env配置
dotenv.load_dotenv()


# 1.定义google_serper工具
class GoogleSerperInput(BaseModel):
    query: str = Field(description="执行谷歌搜索的查询语句")


google_serper_tool = GoogleSerperRun(
    name="google_serper_tool",
    description=(
        "谷歌搜索工具"
        "如果要获取实时内容可以调用这个工具"
        "调用该工具传入搜索关键词相当于完成了一次谷歌搜索"
    ),
    args_schema=GoogleSerperInput,
    api_wrapper=GoogleSerperAPIWrapper()
)


# 2.定义高德IP定位工具
class GaoDeIPLocationInput(BaseModel):
    """IP定位入参"""
    ip: str = Field(description="ip地址")


class GaoDeIPLocationTool(BaseTool):
    """根据IP定位位置工具"""
    name = "ip_location_tool"
    description = "当你需要根据IP，获取定位信息时，可以调用这个工具"
    args_schema = GaoDeIPLocationInput

    def _run(self, ip: str) -> str:
        api_key = os.getenv("GAODE_API_KEY")
        if api_key is None:
            return "请配置GAODE_API_KEY"
        url = "https://restapi.amap.com/v3/ip?ip={ip}&key={key}".format(ip=ip, key=api_key)

        session = requests.session()
        response = session.request(
            method="GET",
            url=url,
            headers={"Content-Type": "application/json; charset=UTF-8"},
        )
        result = response.json()
        return result.get("province") + result.get("city")


ip_location_tool = GaoDeIPLocationTool()

tools = [google_serper_tool, ip_location_tool]

# 3.创建提示词模板
prompt = ChatPromptTemplate.from_messages(
    [("system", "你是实用的聊天助手"),
     ("placeholder", "{chat_history}"),
     ("human", "{input}"),
     ("placeholder", "{agent_scratchpad}")]
)

# 4.创建历史记忆信息
memory = ConversationBufferMemory(
    return_messages=True,
    chat_memory=FileChatMessageHistory("chat_history.txt")
)

# 5.创建LLM
llm = ChatOpenAI(model="gpt-4o", temperature=0)

# 6.创建智能体
agent = create_tool_calling_agent(llm, tools, prompt)

# 7.创建智能体执行者
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 8.调用智能体执行者，进行提问
while True:
    question = input("Human：")
    response = agent_executor.invoke(
        {"input": question, "chat_history": memory.load_memory_variables({})["history"]})
    print(f"AI：" + response.get("output"))
    memory.save_context({"human": question}, {"ai": response.get("output")})
