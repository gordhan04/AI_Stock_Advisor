"""
RAG Engine for Minervini Methodology
Handles document processing, vector storage, and retrieval for stock analysis knowledge base.
"""

import os
from typing import List

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_community.document_loaders import FileSystemBlobLoader
from langchain_community.document_loaders.generic import GenericLoader
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pymupdf4llm import PyMuPDF4LLMParser
from langchain_text_splitters import MarkdownHeaderTextSplitter

# Load environment variables
load_dotenv()

# Configuration
BOOK_PATH = "data/raw"
DB_DIR = "data/processed/chroma"
EMBEDDING_MODEL = "BAAI/bge-base-en-v1.5"


def split_with_markdown_headers(docs: List[Document]) -> List[Document]:
    """
    Split documents using markdown headers for better chunking.

    Args:
        docs: List of documents to split

    Returns:
        List of split documents with metadata
    """
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


def get_vector_db() -> Chroma:
    """
    Initialize or load the vector database for Minervini knowledge base.

    Returns:
        Chroma vector database instance
    """
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    # Load existing database if available
    if os.path.exists(DB_DIR) and os.listdir(DB_DIR):
        return Chroma(
            persist_directory=DB_DIR,
            embedding_function=embeddings
        )

    # Create new database from documents
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


def get_rag_context(question: str, vectordb: Chroma) -> str:
    """
    Retrieve relevant context from the knowledge base for a given question.

    Args:
        question: User's question about stock analysis
        vectordb: Vector database instance

    Returns:
        Concatenated relevant document chunks
    """
    retriever = vectordb.as_retriever(
        search_type="mmr",  # Maximal Marginal Relevance for diversity
        search_kwargs={"k": 4, "fetch_k": 20}
    )

    docs = retriever.invoke(question)

    return "\n\n".join(doc.page_content for doc in docs)

