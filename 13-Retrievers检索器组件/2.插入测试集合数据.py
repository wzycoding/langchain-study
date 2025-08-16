#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2025/8/14 
@Author : wzy
@File   : 2.插入测试集合数据
"""
import dotenv
import weaviate
from langchain_openai import OpenAIEmbeddings
from langchain_weaviate import WeaviateVectorStore

# 读取env配置
dotenv.load_dotenv()

# 1.创建Weaviate客户端
client = weaviate.connect_to_local(
    host="localhost",
    port=8080,
    grpc_port=50051,
)

# 2.创建文本嵌入模型
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# 3.创建Weaviate向量数据库
vector_store = WeaviateVectorStore(
    client=client,
    text_key="text_key",
    embedding=embeddings,
    index_name="Database"
)

# 4.准备好要保存的文本数据、元数据
texts = [
    "光明科技公司总部位于北京市朝阳区，是一家专注于人工智能与大数据分析的高新技术企业，现有员工500人。",
    "董事长张三，男，40岁，籍贯黑龙江漠河市，毕业于清北大学，曾在硅谷工作十年，现负责公司战略规划与重大项目决策。",
    "总经理李四，男，38岁，江苏南京人，拥有十五年软件工程经验，主导过多个国家重点科技项目。",
    "副总经理王五，男，35岁，四川成都人，负责公司运营管理与市场拓展。",
    "技术部拥有120名开发人员，主要从事机器学习模型训练、数据挖掘、云计算平台研发等工作。",
    "光明科技公司在2024年获得国家科技进步二等奖，并与多所高校建立产学研合作关系。",
    "公司设有技术部、市场部、运营部和人力资源部，其中技术部是公司的核心部门。",
    "张三不仅担任董事长，还热衷公益事业，曾多次捐助贫困地区教育项目。",
    "总经理李四毕业于上海交通大学计算机系，擅长分布式系统与云架构设计。",
    "副总经理王五在加入光明科技公司前，曾任某知名互联网企业运营总监，具有丰富的企业管理经验。"
]

metadatas = [
    {"segment_id": "1"},
    {"segment_id": "2"},
    {"segment_id": "3"},
    {"segment_id": "4"},
    {"segment_id": "5"},
    {"segment_id": "6"},
    {"segment_id": "7"},
    {"segment_id": "8"},
    {"segment_id": "9"},
    {"segment_id": "10"},
]

# 5.存储数据到向量数据库
uuids = vector_store.add_texts(texts, metadatas)
