#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2025/12/30 
@Author : wzy
@File   : 1.人工审核
"""
import operator
from typing import TypedDict, Annotated

import dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import AnyMessage, HumanMessage
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.types import Command, interrupt
from psycopg import connect

dotenv.load_dotenv()

# 1.定义llm和工具
llm = init_chat_model(
    "gpt-4o-mini",
    temperature=0
)


# 2.定义State
class State(TypedDict):
    # 图运行的消息列表
    messages: Annotated[list[AnyMessage], operator.add]
    # 发送邮件内容
    email_content: str


# 3.定义大语言模型节点
def llm_node(state: State):
    """调用LLM节点"""
    ai_message = llm.invoke(state["messages"])

    return {"messages": [ai_message], "email_content": ai_message.content}


# 5.核对节点
def check_node(state: State):
    print("======进入人工审核节点======")
    new_email_content = interrupt(f"请核对以下邮件内容,给出最终发送内容：{state['email_content']}")
    return {"email_content": new_email_content}


# 6.构建图
graph = StateGraph(State)

graph.add_node("llm", llm_node)
graph.add_node("check", check_node)

graph.add_edge(START, "llm")
graph.add_edge("llm", "check")
graph.add_edge("check", END)

# 7.创建PostgresSaver检查点管理器
conn = connect("postgres://postgres:postgres@localhost:5432/langgraph", autocommit=True)
checkpointer = PostgresSaver(conn)
checkpointer.setup()

# 8.编译并运行图
agent = graph.compile(checkpointer=checkpointer)
config = {"configurable": {"thread_id": "1"}}
result = agent.invoke(
    {"messages": [HumanMessage(content="写一封邮件给Bob，通知已经给Bob打款10000元货款，邮件格式保持正式信件格式")]},
    config)

# 9.输出中断后返回内容
print(result['__interrupt__'])

# 10.恢复中断执行
state = agent.invoke(Command(resume="你好，Bob，货款10000元已转账，请知悉"), config=config)
print(state['email_content'])
