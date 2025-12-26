from langchain_chroma import Chroma
from embeddings.embedder import get_embedding_model

def create_vectorstore(documents, persist_dir="data/processed/chroma"):
    embeddings = get_embedding_model()

    vectordb = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=persist_dir
    )

    return vectordb
