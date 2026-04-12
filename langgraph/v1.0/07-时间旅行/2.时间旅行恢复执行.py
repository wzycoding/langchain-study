#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2026/1/7 
@Author : wzy
@File   : 2.时间旅行恢复执行
"""
from typing import TypedDict

import dotenv
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.constants import END, START
from langgraph.graph import StateGraph
from psycopg import connect

dotenv.load_dotenv()

# 1.定义llm和工具
llm = init_chat_model(
    "gpt-4o-mini",
    temperature=0
)


# 2.定义图状态数据
class State(TypedDict):
    # 主题
    topic: str
    # 问题
    question: str
    # 回答
    answer: str


# 3.定义生成问题节点
def generate_question_node(state: State):
    """生成问题节点"""
    ai_message = llm.invoke(f"根据{state['topic']}为主题生成一道选择题，难度适中，只需要生成题目，不要输出额外内容。")
    print("======执行generate_question_node=======")
    return {"question": ai_message.content}


# 4.定义生成答案节点
def generate_answer_node(state: State):
    """生成答案节点"""
    ai_message = llm.invoke(f"生成这个问题的答案：{state['question']}，并且给出清晰易懂的解释。")
    print("======执行generate_answer_node=======")
    return {"answer": ai_message.content}


# 5.构建图
graph = StateGraph(State)

graph.add_node("generate_question", generate_question_node)
graph.add_node("generate_answer", generate_answer_node)

graph.add_edge(START, "generate_question")
graph.add_edge("generate_question", "generate_answer")
graph.add_edge("generate_answer", END)

# 6.创建PostgresSaver检查点管理器
conn = connect("postgres://postgres:postgres@localhost:5432/langgraph", autocommit=True)
checkpointer = PostgresSaver(conn)
checkpointer.setup()

# 7.编译并运行图
config = {"configurable": {"thread_id": "100", "checkpoint_id": "1f0eb753-494e-64ea-8001-d5851d91fb48"}}
agent = graph.compile(checkpointer=checkpointer)
new_config = agent.update_state(config, values={"question": "中国有几个直辖市?", "topic": "地理知识"})

state = agent.invoke(None, config=new_config)

# 8.输出图状态数据
print(f"主题：{state['topic']}\n问题：{state['question']}\n答案：{state['answer']}\n")
