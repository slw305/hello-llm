# hello-llm

第一周练习：调用 DeepSeek / 通义千问 API 的基础能力。

## 已实现
- Day1 首个调用 / Day3 参数实验(temperature/max_tokens)
- Day4 多轮对话 / Day5 JSON结构化输出
- Day6 双模型对比 / Day7 简历优化助手(Prompt工程)
- Day8 流式输出(SSE)

## 环境
Python 3.13 + uv 管理依赖（依赖在 pyproject.toml / uv.lock）

## 使用
uv sync                      # 安装依赖
# 用 Jupyter / PyCharm 打开 hello_deepseek.ipynb 逐个运行

## 环境变量
见 .env.example（DEEPSEEK_API_KEY / DASHSCOPE_API_KEY）