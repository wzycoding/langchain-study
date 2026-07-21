#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""让 LangChain Agent 使用本地 MCP Server 提供的天气工具。"""

import asyncio
import sys
from pathlib import Path

import dotenv
from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient


SERVER_FILE = Path(__file__).with_name("13.1 MCP Server.py")


async def main() -> None:
    dotenv.load_dotenv()

    # MultiServerMCPClient 会按配置启动 MCP Server，并把 MCP 工具转换为 LangChain 工具。
    client = MultiServerMCPClient(
        {
            "weather": {
                "transport": "stdio",
                "command": sys.executable,
                "args": [str(SERVER_FILE)],
            }
        }
    )
    tools = await client.get_tools()

    agent = create_agent(
        model="deepseek-v4-flash",
        tools=tools,
        system_prompt="你是一个天气助手，只能使用天气工具回答天气问题。",
    )
    result = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "请查询杭州今天的天气"}]}
    )
    print(result["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
