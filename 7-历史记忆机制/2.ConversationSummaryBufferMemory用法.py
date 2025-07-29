#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2025/7/29 
@Author : wzy
@File   : 2.ConversationSummaryBufferMemory用法
"""
from operator import itemgetter

import dotenv
from langchain.memory import ConversationSummaryBufferMemory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_openai import ChatOpenAI

# 读取env配置
dotenv.load_dotenv()

# 1.创建提示词模板
prompt = ChatPromptTemplate.from_messages([
    MessagesPlaceholder("chat_history"),
    ("human", "{question}"),
])

# 2.构建GPT-3.5模型
llm = ChatOpenAI(model="gpt-3.5-turbo")

# 3.创建输出解析器
parser = StrOutputParser()

memory = ConversationSummaryBufferMemory(return_messages=True,
                                         max_token_limit=200,
                                         llm=ChatOpenAI(model="gpt-3.5-turbo")
                                         )

# 4.执行链
chain = RunnablePassthrough.assign(
    chat_history=(RunnableLambda(memory.load_memory_variables) | itemgetter("history"))
) | prompt | llm | parser

while True:
    print("========================")
    question = input("Human：")
    response = chain.invoke({"question": question})
    print(f"AI：{response}")
    memory.save_context({"human": question}, {"ai": response})
    print("========================")
    print(f"对话历史信息：{memory.load_memory_variables({})}")
