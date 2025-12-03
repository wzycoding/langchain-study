#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2025/7/20 
@Author : wzy
@File   : 3.其他大语言模型使用
"""
import dotenv
from langchain_community.chat_models import ChatTongyi
from langchain_core.prompts import PromptTemplate
# 读取env配置
dotenv.load_dotenv()

# 1.构建提示词
prompt = PromptTemplate.from_template("{question}")

# 2.构建通义模型
tongyi_chat = ChatTongyi(
    model="qwen-turbo-2025-04-28"
)

prompt_value = prompt.invoke({"question": "请完整输出短歌行"})

# 3.文本生成模型接受promptValue，并输出结果
print(tongyi_chat.invoke(prompt_value).content)
