# -------- RAG ENGINE (Removed LLM and used agent ) --------

from langchain_pymupdf4llm import PyMuPDF4LLMParser
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv
import os

from langchain_community.document_loaders import FileSystemBlobLoader
from langchain_community.document_loaders.generic import GenericLoader
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_core.documents import Document

load_dotenv()

BOOK_PATH = "data/raw"
DB_DIR = "data/processed/chroma"


# ---------------- SPLITTER ----------------
def split_with_markdown_headers(docs):
    splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=[
            ("##", "section"),
            ("###", "subsection"),
        ]
    )

    final_docs = []

    for doc in docs:
        splits = splitter.split_text(doc.page_content)
        for split in splits:
            final_docs.append(
                Document(
                    page_content=split.page_content,
                    metadata={**(doc.metadata or {}), **split.metadata}
                )
            )

    return final_docs


# ---------------- VECTOR DB ----------------
def get_vector_db():
    embeddings = HuggingFaceEmbeddings(
        model_name="BAAI/bge-base-en-v1.5"
    )

    if os.path.exists(DB_DIR) and os.listdir(DB_DIR):
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

    documents = loader.load()
    chunks = split_with_markdown_headers(documents)

    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=DB_DIR
    )

    return vectordb


# ---------------- RAG CONTEXT ONLY ----------------
def get_rag_context(question: str, vectordb) -> str:
    retriever = vectordb.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 4, "fetch_k": 20}
    )

    docs = retriever.invoke(question)

    return "\n\n".join(d.page_content for d in docs)

