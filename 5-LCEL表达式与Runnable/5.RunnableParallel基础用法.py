#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2025/7/24 
@Author : wzy
@File   : 5.RunnableParallel基础用法
"""
import dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel
from langchain_openai import ChatOpenAI

# 读取env配置
dotenv.load_dotenv()

# 1.构建提示词
chinese_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个资深文学家"),
    ("human", "请以{subject}为主题写一首古诗")
])

math_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个资深数学家"),
    ("human", "请你给出数学问题:{question}的答案")
])

# 2.创建模型
llm = ChatOpenAI()
# 3.创建字符串输出解析器
parser = StrOutputParser()

# 4.创建并行链
parallel_chain = RunnableParallel({
    "chinese": chinese_prompt | llm | parser,
    "math": math_prompt | llm | parser
})

# 5.执行链
print(f"输出结果：{parallel_chain.invoke({'subject': '春天', 'question': '24和16最大公约数是多少？'})}")
