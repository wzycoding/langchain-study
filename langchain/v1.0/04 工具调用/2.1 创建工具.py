#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2026/6/9 
@Author : wzy
@File   : 2.1 创建工具
"""
from langchain.tools import tool


@tool("search_ip_location", description="通过用户提供的ip地址，获取对应地理位置")
def get_ip_location(ip: str) -> str:
    """通过ip地址获取位置信息

    Args:
        ip: 要查询定位的ip地址
    """
    return f"ip地址：{ip}，定位地址：浙江杭州"
