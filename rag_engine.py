# All LangChain / RAG code
import os

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

BOOK_PATH = "data/raw/minervini_book.pdf"
DB_DIR = "data/processed/chroma"

PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     "You are a stock analyst strictly following Mark Minervini methodology."),
    ("human",
     "Stock Data:\n{stock_context}\n\n"
     "Minervini Reference:\n{rag_context}\n\n"
     "Question:\n{question}")
])

def get_vector_db():
    embeddings = HuggingFaceEmbeddings(
        model_name="BAAI/bge-base-en-v1.5"
    )

    if os.path.exists(DB_DIR):
        return Chroma(
            persist_directory=DB_DIR,
            embedding_function=embeddings
        )

    loader = PyPDFLoader(BOOK_PATH)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=100
    )
    chunks = splitter.split_documents(docs)

    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=DB_DIR
    )
    return vectordb

def explain_with_rag(question, stock_context, vectordb):
    retriever = vectordb.as_retriever(search_kwargs={"k": 4})

    docs = retriever.invoke(question)
    rag_context = "\n\n".join(d.page_content for d in docs)

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    )

    messages = PROMPT.invoke({
        "stock_context": stock_context,
        "rag_context": rag_context,
        "question": question
    })

    response = llm.invoke(messages)
    return response.content
