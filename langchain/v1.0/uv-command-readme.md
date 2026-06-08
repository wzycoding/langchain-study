# 初始化项目

uv init

# 创建虚拟环境

uv venv

# 安装依赖

uv add langchain langgraph openai

# 安装开发工具

uv add --dev pytest ruff

# 同步依赖

uv sync

# 运行项目

uv run python main.py

# 运行 LangGraph

uv run langgraph dev

# 更新依赖

uv lock --upgrade

# 删除依赖

uv remove xxx

# 安装 Python

uv python install 3.12

# 固定 Python 版本

uv python pin 3.12