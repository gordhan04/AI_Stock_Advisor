# All LangChain / RAG code
import os

from langchain_pymupdf4llm import PyMuPDF4LLMParser
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os
load_dotenv()

if not os.getenv("GROQ_API_KEY"):
    raise ValueError("GROQ_API_KEY not found. Please check your .env file.")

BOOK_PATH = "data/raw"
DB_DIR = "data/processed/chroma"
from langchain_community.document_loaders import FileSystemBlobLoader
from langchain_community.document_loaders.generic import GenericLoader
from langchain_pymupdf4llm import PyMuPDF4LLMParser
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_core.documents import Document


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

    loader = GenericLoader(
            blob_loader=FileSystemBlobLoader(
                path=BOOK_PATH,
                glob="*.pdf",
            ),
            blob_parser=PyMuPDF4LLMParser(),
            )
    
    def split_with_markdown_headers(docs):
        splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=[
                ("##", "section"),
                ("###", "subsection"),
            ]
        )

        final_docs = []

        for doc in docs:
            # 1️⃣ Split TEXT, not Document
            splits = splitter.split_text(doc.page_content)

            # 2️⃣ Convert back to Document objects
            for split in splits:
                final_docs.append(
                    Document(
                        page_content=split.page_content,
                        metadata={**doc.metadata, **split.metadata}
                    )
                )

        return final_docs
    documents = loader.load()
    chunks = split_with_markdown_headers(documents)

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

    llm = ChatGroq(
        model="openai/gpt-oss-20b",
        temperature=0,
        max_tokens=None,
        reasoning_format="parsed",
        timeout=None,
        max_retries=2,
    )

    messages = PROMPT.invoke({
        "stock_context": stock_context,
        "rag_context": rag_context,
        "question": question
    })

    response = llm.invoke(messages)
    return response.content
