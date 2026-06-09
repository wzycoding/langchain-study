#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2026/6/9 
@Author : wzy
@File   : 3.2 Message的内容
"""

import dotenv
from langchain.messages import HumanMessage

dotenv.load_dotenv()

# 人类消息
# 传递字符串
human_message = HumanMessage("你好你是")

# 通过content传递多模态信息
human_message = HumanMessage(content=[
    {"type": "text", "text": "这张图片是哪个动漫人物？"},
    {"type": "image", "url": "https://image.baidu.com/a.jpg"}
])

# 通过content_block传递多模态信息
human_message = HumanMessage(content_blocks=[
    {"type": "text", "text": "这张图片是哪个动漫人物？"},
    {"type": "image", "url": "https://image.baidu.com/a.jpg"}
])
