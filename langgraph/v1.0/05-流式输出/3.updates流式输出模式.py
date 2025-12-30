#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2025/12/26 
@Author : wzy
@File   : 3.updates流式输出模式
"""

import operator
from typing import TypedDict, Annotated

import dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import AnyMessage, HumanMessage, SystemMessage
from langgraph.constants import END, START
from langgraph.graph import StateGraph

dotenv.load_dotenv()

# 1.定义llm和工具
llm = init_chat_model(
    "gpt-4o-mini",
    temperature=0
)


# 2.定义State
class MessagesState(TypedDict):
    # 图运行的消息列表
    messages: Annotated[list[AnyMessage], operator.add]
    query: str
    retrival_result: Annotated[list[str], operator.add]


# 3.定义检索节点a
def retrival_a_node(state: MessagesState):
    """调用数据检索a节点"""
    # todo：模拟根据query进行数据检索
    return {
        "retrival_result": [
            "A公司（Company A）成立于2015年，总部位于上海，是一家专注于智能家居和物联网解决方案的高科技企业。公司使命是“让科技融入生活，提高家庭智能化水平”。" +
            "A公司致力于通过物联网技术连接家庭设备，实现智能控制与能源优化，为用户提供舒适、安全、节能的家居体验。"]
    }


# 4.定义检索节点b
def retrival_b_node(state: MessagesState):
    """调用数据检索b节点"""
    # todo：模拟根据query进行数据检索
    return {
        "retrival_result": [
            """
                主要业务与产品：
                - 智能家居控制系统：支持语音、手机APP远程控制家电和照明设备。
                - 家庭安全监控设备：智能摄像头、门窗传感器及报警系统。
                - 能源管理平台：智能插座、智能照明及家电能耗分析。
                - 定制化物联网解决方案：为房地产、酒店等提供智能化方案。
                
                核心竞争力：
                - 自主研发的AI算法与物联网通信技术。
                - 完整的软硬件生态系统。
                - 强大的客户服务与售后体系。
                - 多项智能家居专利技术。
                
                发展历程：
                - 2015年：公司成立，初期聚焦智能插座和照明设备。
                - 2016年：推出首款智能家居控制系统，获得天使轮融资。
                - 2018年：完成B轮融资，引入战略投资者。
                - 2020年：产品线扩展至家庭安防及能源管理领域。
                - 2022年：进入海外市场，主要面向东南亚和欧洲。
                - 2023年：用户数量突破100万，市值估计达5亿美元。
            """
        ]
    }


# 5.定义llm节点
def llm_node(state: MessagesState):
    """调用LLM节点"""
    system_prompt = """
        你是一个公司内部的智能助手，只能回答跟公司A有关的问题，你可以根据知识库检索信息进行问题的回答，不能凭空捏造答案
        检索到的知识库信息如下：{retrival_info}
    """
    retrival_info = ""
    for retrival_item in state["retrival_result"]:
        retrival_info += retrival_item + "\n"
    system_message = SystemMessage(content=system_prompt.format(retrival_info=retrival_info))
    ai_message = llm.invoke([system_message, *state["messages"]])

    return {"messages": [ai_message]}


# 7.构建图
graph = StateGraph(MessagesState)

graph.add_node("llm", llm_node)
graph.add_node("retrival_a", retrival_a_node)
graph.add_node("retrival_b", retrival_b_node)

graph.add_edge(START, "retrival_a")
graph.add_edge("retrival_a", "retrival_b")
graph.add_edge("retrival_b", "llm")
graph.add_edge("llm", END)

# 8.编译并运行图
agent = graph.compile()

query = "你好，A公司是一家有实力的公司吗？"

# updates模式
for chunk in agent.stream({"messages": [HumanMessage(content=query)],
                           "query": query}, stream_mode="updates"):
    print(chunk)
