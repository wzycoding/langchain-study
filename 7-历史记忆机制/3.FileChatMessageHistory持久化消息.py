#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2025/7/29 
@Author : wzy
@File   : 3.FileChatMessageHistory持久化消息
"""
from operator import itemgetter

import dotenv
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_message_histories import FileChatMessageHistory
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

memory = ConversationBufferMemory(
    return_messages=True,
    chat_memory=FileChatMessageHistory("chat_history.txt")
)

# 4.执行链
chain = RunnablePassthrough.assign(
    chat_history=(RunnableLambda(memory.load_memory_variables) | itemgetter("history"))
) | prompt | llm | parser

while True:
    question = input("Human：")
    response = chain.invoke({"question": question})
    print(f"AI：{response}")
    memory.save_context({"human": question}, {"ai": response})
