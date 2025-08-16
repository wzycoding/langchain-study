#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2025/8/14 
@Author : wzy
@File   : 1.删除测试集合数据
"""
import weaviate

client = weaviate.connect_to_local(
    host="localhost",
    port=8080,
    grpc_port=50051,
)

# 删除集合
client.collections.delete(
    "Database"
)
