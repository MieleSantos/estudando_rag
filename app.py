"""
dados ficam em memoria
"""

import os
from langchain import hub
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pprint import pprint

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("API_KEY")

model = ChatOpenAI(model="gpt-4")

pdf_path = "laptop_manual.pdf"
loader = PyMuPDFLoader(pdf_path)
docs = loader.load()


text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

chunks = text_splitter.split_documents(documents=docs)


embedding = OpenAIEmbeddings()
# criando banco em memoria
vector_store = Chroma.from_documents(
    documents=chunks, embedding=embedding, collection_name="laptp_manual"
)


# criando recuperador de informação
retriever = vector_store.as_retriever()
# result = retriever.invoke("Qual é a bateria do notebook")

prompt = hub.pull("rlm/rag-prompt")

rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)
# question = "como funciona o cancelamento de ruido inteligente"
# response = rag_chain.invoke(question)
# pprint(response)

try:
    while True:
        question = input("Qual a sua duvida? ")
        response = rag_chain.invoke(question)
        pprint(response)
except KeyboardInterrupt:
    exit()
