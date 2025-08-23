#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2025/8/22 
@Author : wzy
@File   : 1.构建ReACT架构Agent
"""
import os

import dotenv
import requests
from langchain.agents import create_react_agent, AgentExecutor
from langchain_community.tools import GoogleSerperRun
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import BaseTool, render_text_description_and_args
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
prompt = ChatPromptTemplate.from_template(
    "Answer the following questions as best you can. You have access to the following tools:\n\n"
    "{tools}\n\n"
    "Use the following format:\n\n"
    "Question: the input question you must answer\n"
    "Thought: you should always think about what to do\n"
    "Action: the action to take, should be one of [{tool_names}]\n"
    "Action Input: the input to the action\n"
    "Observation: the result of the action\n"
    "... (this Thought/Action/Action Input/Observation can repeat N times)\n"
    "Thought: I now know the final answer\n"
    "Final Answer: the final answer to the original input question\n\n"
    "Begin!\n\n"
    "Question: {input}\n"
    "Thought:{agent_scratchpad}"
)

# 4.创建LLM
llm = ChatOpenAI(model="gpt-4o", temperature=0)

# 5.创建智能体
agent = create_react_agent(
    llm=llm,
    prompt=prompt,
    tools=tools,
    tools_renderer=render_text_description_and_args,
)

# 6.创建智能体执行者
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 7.调用智能体执行者，进行提问
print(agent_executor.invoke({"input": "北京今天天气预报"}))
