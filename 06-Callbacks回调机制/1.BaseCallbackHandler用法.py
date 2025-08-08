#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2025/7/26 
@Author : wzy
@File   : 1.BaseCallbackHandler用法
"""
from typing import Dict, Any, Optional, List
from uuid import UUID

import dotenv
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.messages import BaseMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.outputs import LLMResult
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()


class CustomCallbackHandler(BaseCallbackHandler):
    """自定义回调处理类"""

    def on_chat_model_start(self, serialized: Dict[str, Any], messages: List[List[BaseMessage]], *, run_id: UUID,
                            parent_run_id: Optional[UUID] = None, tags: Optional[List[str]] = None,
                            metadata: Optional[Dict[str, Any]] = None, **kwargs: Any) -> Any:
        print("======聊天模型结束执行======")

    def on_llm_end(self, response: LLMResult, *, run_id: UUID, parent_run_id: Optional[UUID] = None,
                   **kwargs: Any) -> Any:
        print("======聊天模型结束执行======")

    def on_chain_start(self, serialized: Dict[str, Any], inputs: Dict[str, Any], *, run_id: UUID,
                       parent_run_id: Optional[UUID] = None, tags: Optional[List[str]] = None,
                       metadata: Optional[Dict[str, Any]] = None, **kwargs: Any) -> Any:
        print(f"开始执行当前组件{kwargs['name']}，run_id: {run_id}, 入参：{inputs}")

    def on_chain_end(self, outputs: Dict[str, Any], *, run_id: UUID, parent_run_id: Optional[UUID] = None,
                     **kwargs: Any) -> Any:
        print(f"结束执行当前组件，run_id: {run_id}, 执行结果：{outputs}, {kwargs}")


# 1.创建提示词模板
prompt = ChatPromptTemplate.from_template("{question}")

# 2.构建GPT-3.5模型
llm = ChatOpenAI(model="gpt-3.5-turbo")

# 3.创建输出解析器
parser = StrOutputParser()

# 4.执行链
chain = prompt | llm | parser
chain.invoke({"question": "请输出静夜思的原文"},
             {"callbacks": [CustomCallbackHandler()]})
