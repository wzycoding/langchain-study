#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2025/7/19 
@Author : wzy
@File   : 7.完整示例
"""
from datetime import datetime

import dotenv
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

# 读取env配置
dotenv.load_dotenv()
# 1.构建提示词
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是OpenAI开发的大语言模型，对我的提问进行回答"),
    MessagesPlaceholder("memory"),
    ("human", "{question}"),
    ("human", "{currentTime}")
]).partial(currentTime=datetime.now())

# 2.构建GPT-3.5模型
llm = ChatOpenAI(model="gpt-3.5-turbo")

# 3.创建输出解析器
parser = StrOutputParser()

# 4.执行链
chain = chat_prompt | llm | parser

print(chain.invoke({"question": "你是谁，现在是哪一年，请问今年最好的手机品牌是什么？",
                    "memory": [HumanMessage("你是小米公司的雷军，你扮演雷军的身份和我对话"),
                               AIMessage("好的我是小米公司的雷军，下面将会以雷军的身份和口吻回答你的问题")]}))
