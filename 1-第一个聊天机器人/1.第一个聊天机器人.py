#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2025/7/15 
@Author : wzy
@File   : 1.第一个聊天机器人
"""
import dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# 读取env配置
dotenv.load_dotenv()

# 1.创建提示词模板
prompt = ChatPromptTemplate.from_template("{question}")

# 2.构建GPT-3.5模型
llm = ChatOpenAI(model="gpt-3.5-turbo")

# 3.创建输出解析器
parser = StrOutputParser()

# 4.执行链
chain = prompt | llm | parser
print(chain.invoke({"question": "请以表格的形式返回三国演义实力最强的十个人，并进行简要介绍"}))


