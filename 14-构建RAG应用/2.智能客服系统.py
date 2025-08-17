#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2025/8/17 
@Author : wzy
@File   : 2.智能客服系统
"""
from operator import itemgetter

import dotenv
import weaviate
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_message_histories import FileChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_weaviate import WeaviateVectorStore

# 读取env配置
dotenv.load_dotenv()

# 1.创建提示词模板
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是大米公司的智能客服，你的名字叫大米，接下来你将扮演一个专业客服的角色，对用户提出来的商品问题进行回答，一定要礼貌热情，"
                   "如果用户提问与客服和商品无关的问题，礼貌委婉的表示拒绝或无法回答，只回答商品售卖相关的问题"),
        MessagesPlaceholder("chat_history"),
        ("human", """
            用户提问上下文信息：
            <context>{context}</context>
            请根据用户提出的问题进行回答：{query}
        """)
    ]
)

# 2.构建GPT-3.5模型
llm = ChatOpenAI(model="gpt-3.5-turbo")

# 3.创建输出解析器
parser = StrOutputParser()

# 4.构建检索器
client = weaviate.connect_to_local(
    host="localhost",
    port=8080,
    grpc_port=50051,
)
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

vector_store = WeaviateVectorStore(
    client=client,
    text_key="text_key",
    embedding=embeddings,
    index_name="Product"
)
retriever = vector_store.as_retriever(search_kwargs={"k": 1})

# 5.创建记忆组件
memory = ConversationBufferMemory(
    return_messages=True,
    chat_memory=FileChatMessageHistory("customer_service_history.txt")
)


def format_documents(documents) -> str:
    return "\n".join([document.page_content for document in documents])


# 6.构建链
chain = ({"context": retriever | format_documents, "query": RunnablePassthrough()}
         | RunnablePassthrough.assign(
            chat_history=(RunnableLambda(memory.load_memory_variables) | itemgetter("history")))
         | prompt | llm | parser)

while True:

    query = input("用户：")
    if query == '退出':
        exit(0)
    # 7.调用链，开始对话
    response = chain.stream(query)
    print("智能客服： ", flush=True, end="")

    answer = ""
    for chunk in response:
        answer += chunk
        print(chunk, flush=True, end="")
    print()

    # 8.存储对话信息
    memory.save_context({"用户": query}, {"智能客服": answer})
