#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2026/6/10 
@Author : wzy
@File   : 2.7 获取流输出器
"""
import dotenv
import time
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain.tools import tool, ToolRuntime

dotenv.load_dotenv()


# 1.定义工具
@tool
def generate_ppt(runtime: ToolRuntime, subject: str):
    """生成ppt"""
    writer = runtime.stream_writer
    writer(f"第1步：开始解析主题{subject}")
    time.sleep(3)
    writer(f"第2步：查找模板库")
    time.sleep(3)
    writer(f"第3步：布局排版")
    time.sleep(3)
    writer(f"第4步：最终检查")
    time.sleep(3)
    writer(f"第5步：输出文件")

    return f"{subject}.ppt"


# 2.创建Agent
agent = create_agent(model="deepseek-v4-flash",
                     system_prompt="你是一个专门为程序员工作的AI助手",
                     tools=[generate_ppt])

# 3.调用Agent
for chunk in agent.stream({
    "messages": [
        HumanMessage("生成一个主题为儿童节的ppt")
    ]
}, stream_mode=["updates", "custom"]):
    print(chunk)


