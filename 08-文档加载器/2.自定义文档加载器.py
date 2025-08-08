#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2025/8/3 
@Author : wzy
@File   : 2.自定义文档加载器
"""
from typing import List

from langchain_core.document_loaders import BaseLoader
from langchain_core.documents import Document


class ChatRecordLoader(BaseLoader):
    file_path: str

    def __init__(self, file_path: str):
        self.file_path = file_path

    def load(self) -> List[Document]:
        """加载聊天记录文档"""
        documents = []
        with open(self.file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                # 如果包含中文冒号，则进行分割
                if "：" in line:
                    user_name, content = line.split("：", 1)
                    documents.append(
                        Document(
                            page_content=content.strip(),
                            metadata={"user_name": user_name.strip()}
                        )
                    )
                else:
                    # 不符合格式要求直接跳过
                    continue
        return documents


chat_record_loader = ChatRecordLoader(file_path="chat_record.txt")
documents = chat_record_loader.load()
print(f"文档数量：{len(documents)}")
for document in documents:
    print(f"文档内容：{document.page_content}")
    print(f"文档元数据：{document.metadata}")
