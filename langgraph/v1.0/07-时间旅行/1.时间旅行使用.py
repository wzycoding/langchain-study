#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2026/1/3 
@Author : wzy
@File   : 1.时间旅行使用
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

    return {"question": ai_message.content}


# 4.定义生成答案节点
def generate_answer_node(state: State):
    """生成答案节点"""
    ai_message = llm.invoke(f"生成这个问题的答案：{state['question']}，并且给出简单详细的解释。")

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
config = {"configurable": {"thread_id": "100"}}
agent = graph.compile(checkpointer=checkpointer)
state = agent.invoke({"topic": "英语可数名词与不可数名词"}, config=config)

# 8.输出图状态数据
print(f"主题：{state['topic']}\n问题：{state['question']}\n 答案：{state['answer']}\n")

# 9.获取历史检查点信息
states = list(agent.get_state_history(config))

for state in states:
    print(f"下一个节点：{state.next}")
    print(state.config["configurable"]["checkpoint_id"])
    print()
