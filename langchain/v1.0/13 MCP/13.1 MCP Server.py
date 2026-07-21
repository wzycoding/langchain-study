#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""创建一个通过 stdio 通信的天气 MCP Server。"""

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("weather-server")


@mcp.tool()
def get_weather(city: str) -> str:
    """查询指定城市的天气。

    Args:
        city: 城市名称。
    """
    return f"{city}今天晴，气温 22°C 到 29°C。"


if __name__ == "__main__":
    mcp.run(transport="stdio")
