#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2025/12/30 
@Author : wzy
@File   : 1.人工审核
"""
from typing import TypedDict, Literal

import dotenv
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.types import interrupt, Command
from psycopg import connect

dotenv.load_dotenv()


# 1.定义State
class State(TypedDict):
    # 支付金额
    pay_amount: int
    # 收款公司
    receiving_company: str
    # 是否通过审核
    approved: bool


# 2.定义支付节点
def pay_node(state: State):
    print("======进入支付节点======")
    approved = interrupt(f"你是否允许给{state['receiving_company']}打款{state['pay_amount']}元？")

    if approved:
        print("======人工审核通过，支付成功======")
    else:
        print("======人工审核拒绝，支付失败======")
    return {"approved": approved}


# 3.生成账单节点
def generate_bill_node(state: State):
    print("======开始生成账单======")


# 4.定义条件边路由函数
def pay_route(state: State) -> Literal["generate_bill", END]:
    if state['approved']:
        return "generate_bill"
    return END


# 5.构建编译图
graph = StateGraph(State)

graph.add_node("pay", pay_node)
graph.add_node("generate_bill", generate_bill_node)

graph.add_edge(START, "pay")
graph.add_conditional_edges("pay", pay_route, ["generate_bill", END])

# 6.创建PostgresSaver检查点管理器
conn = connect("postgres://postgres:postgres@localhost:5432/langgraph", autocommit=True)
checkpointer = PostgresSaver(conn)
checkpointer.setup()

# 7.编译并运行图
agent = graph.compile(checkpointer=checkpointer)
config = {"configurable": {"thread_id": "1"}}
result = agent.invoke({"pay_amount": "6000", "receiving_company": "大米科技有限公司"}, config)

# 8.输出中断后返回内容
print(result)

# 9.恢复中断执行
agent.invoke(Command(resume=False), config=config)
