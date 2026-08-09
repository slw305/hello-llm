from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings,ChatOpenAI
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os,glob

load_dotenv()

#----加载----
def load_text(path:str):
    with open(path,encoding="utf-8") as f:
        text=f.read()
    return Document(page_content=text,metadata={"source":path})

all_docs = []
for f in glob.glob("data/*.md"):
    all_docs.append(load_text(f))
print("文档数:",len(all_docs))

#----分块----
splitter = RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=50)
chunks = splitter.split_documents(all_docs)
print("分块数:",len(chunks))

#----向量化+入库----
embeddings = OpenAIEmbeddings(
    model="BAAI/bge-m3",
    api_key=os.getenv("SILICONFLOW_API_KEY"),
    base_url="https://api.siliconflow.cn/v1"
)
vectorstore = Chroma(
    collection_name="my_notes",
    embedding_function=embeddings,
    persist_directory="chroma_db"
)
if vectorstore._collection.count() == 0:
    vectorstore.add_documents(chunks)

retriever = vectorstore.as_retriever(search_kwargs={"k":3})

#----检索+拼prompt+回答----
def ask(question:str)->str:
    docs = retriever.invoke(question)  #检索
    context = "\n\n".join(d.page_content for d in docs)  #拼上下文

    prompt = ChatPromptTemplate.from_messages([
        ("system","你是一个知识库问答助手。只根据下面的资料回答，资料里没有就说不知道。\n\n资料：\n{context}"),
        ("user","{question}"),
    ])
    llm = ChatOpenAI(
        model="deepseek-v4-flash",
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com",
        temperature=0.3,
        max_tokens=500
    )

    chain = prompt|llm|StrOutputParser()

    return chain.invoke({"context":context,"question":question})  #回答

if __name__ == "__main__":
    print("RAG问答demo(输入exit退出)")
    while True:
        q = input("请输入问题：").strip()
        if q.lower() == "exit":
            break
        print("回答：",ask(q))
        print()