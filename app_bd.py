"""
Persistindo dados em um banco de dados
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


persist_directory = "db"

embedding = OpenAIEmbeddings()

vector_store = Chroma.from_documents(
    documents=chunks,
    embedding=embedding,
    persist_directory=persist_directory,
    collection_name="laptop_manual",
)
