# hello-llm

第一周练习：调用 DeepSeek / 通义千问 API 的基础能力。

## 已实现
- Day1 首个调用 / Day3 参数实验(temperature/max_tokens)
- Day4 多轮对话 / Day5 JSON结构化输出
- Day6 双模型对比 / Day7 简历优化助手(Prompt工程)
- Day8 流式输出(SSE)
- Day10 langchain调用跑通
- Day11 ChatPromptTemplate模板练习
- Day12 Pydantic校验+结构化提取
- Day13 LCEL管道chain跑通
- Day14 带记忆对话助手(手动记忆)
- Day15 add工具+agent跑通
- Day16 术语解释器+复盘推GitHub
- Day17-23 RAG全流程、Chroma检索、LangSmith调试
- ```mermaid
flowchart LR
    A[文档] --> B[加载 Document]
    B --> C[分块 chunk_size=500]
    C --> D[向量化 BGE]
    D --> E[(Chroma 向量库)]
    F[问题] --> G[向量化]
    G --> H[相似度检索 k=3]
    E --> H
    H --> I[拼 context 进 prompt]
    I --> J[DeepSeek 回答]
```
## 环境
Python 3.13 + uv 管理依赖（依赖在 pyproject.toml / uv.lock）

## 使用
uv sync                      # 安装依赖
# 用 Jupyter / PyCharm 打开 ***.ipynb 逐个运行

## 环境变量
见 .env.example（DEEPSEEK_API_KEY / DASHSCOPE_API_KEY）