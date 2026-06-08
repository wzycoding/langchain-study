#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2026/6/8 
@Author : wzy
@File   : 2.8 结构化输出
"""
import dotenv
from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field

dotenv.load_dotenv()


class Song(BaseModel):
    """歌曲信息类"""
    song_name: str = Field(description="歌曲名称")
    singer: str = Field(description="歌手")


class SongList(BaseModel):
    """歌曲列表"""
    songs: list[Song] = Field(description="歌曲列表")


# 1.创建model对象
model = init_chat_model(
    "gpt-4o"
)

with_structured_model = model.with_structured_output(SongList)

# 2.调用大模型，返回AIMessage
print(with_structured_model.invoke("请输出5首中文流行歌曲"))
