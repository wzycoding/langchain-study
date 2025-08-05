#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2025/8/4 
@Author : wzy
@File   : 1.RecursiveCharacterTextSplitter用法
"""
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 1.分割文本内容
content = ("李白（701年2月28日~762年12月），字太白，号青莲居士，出生于蜀郡绵州昌隆县（今四川省绵阳市江油市青莲镇），一说山东人，一说出生于西域碎叶，祖籍陇西成纪（今甘肃省秦安县）。"
           ""
           "唐代伟大的浪漫主义诗人，被后人誉为“诗仙”，与杜甫并称为“李杜”，为了与另两位诗人李商隐与杜牧即“小李杜”区别，杜甫与李白又合称“大李杜”。"
           ""
           "据《新唐书》记载，李白为兴圣皇帝（凉武昭王李暠）九世孙，与李唐诸王同宗。其人爽朗大方，爱饮酒作诗，喜交友。"
           ""
           "李白深受黄老列庄思想影响，有《李太白集》传世，诗作中多为醉时写就，代表作有《望庐山瀑布》《行路难》《蜀道难》《将进酒》《早发白帝城》等")

# 2.定义递归文本分割器
text_splitter = RecursiveCharacterTextSplitter(chunk_size=100,
                                               chunk_overlap=30,
                                               length_function=len,
                                               )

# 3.分割文本
splitter_texts = text_splitter.split_text(content)

# 4.转换为文档对象
splitter_documents = text_splitter.create_documents(splitter_texts)

print(f"分割文档数量：{len(splitter_documents)}")
for splitter_document in splitter_documents:
    print(f"文档片段大小：{len(splitter_document.page_content)}, 文档元数据：{splitter_document.metadata}")
