import os
from dotenv import load_dotenv
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma


load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("API_KEY")
model = ChatOpenAI(model="gpt-4")

persist_directory = "db"

embedding = OpenAIEmbeddings()

# preparando banco para operações de crud
vectot_store = Chroma(
    persist_directory=persist_directory,
    embedding_function=embedding,
    collection_name="laptop_manual",
)

retriever = vectot_store.as_retriever()

system_prompt = """
Use o contexto para responder as perguntas.
Contexto: {context}
"""

prompt = ChatPromptTemplate([("system", system_prompt), ("human", "{input}")])

# criando o chain
question_answer_chain = create_stuff_documents_chain(llm=model, prompt=prompt)

# chain usando o retrierver
chain = create_retrieval_chain(
    retriever=retriever, combine_docs_chain=question_answer_chain
)

query = "qual a marca do modelo do notebook?"

response = chain.invoke({"input": query})
print(response)
