#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2025/8/11 
@Author : wzy
@File   : 1.连接Weaviate数据库
"""
import weaviate

client = weaviate.connect_to_local(
    host="localhost",
    port=8080,
    grpc_port=50051,
)

print(client.is_ready())
