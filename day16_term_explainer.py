from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os

load_dotenv()


# 1.定义输出结构
class TermExplanation(BaseModel):
    term: str = Field(description="术语名称")
    one_sentence: str = Field(description="一句话解释")
    detail: str = Field(description="详细解释，2-3句话")
    example: str = Field(description="一个代码或生活类比示例")


# 2.解析器+模板
parser = PydanticOutputParser(pydantic_object=TermExplanation)

prompt = ChatPromptTemplate.from_messages([("system", "你是资深编程导师。严格按下面的格式输出:\n{format_instructions}"),
                                           ("user", "请解释编程术语：{term}") ]).partial(format_instructions=parser.get_format_instructions())

# 3.模型
llm = ChatOpenAI(
    model="deepseek-v4-flash",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
    temperature=0.3,
    max_tokens=500
)

# 4.管道
chain = prompt | llm | parser

# 5.主循环(命令行交互)
if __name__ == "__main__":
    print("术语解释器v1(输入exit退出)")
    while True:
        term = input("请输入术语：").strip()
        if term.lower() == "exit":
            break
        try:
            exp = chain.invoke({"term":term})
            print(f"\n术语：{exp.term}")
            print(f"一句话：{exp.one_sentence}")
            print(f"详解：{exp.detail}")
            print(f"示例：{exp.example}\n")
        except Exception as e:
            print(f"这次解析失败了，换个问法试试。错误：{e}\n")
