def get_retriever(vectordb, k=4):
    return vectordb.as_retriever(search_kwargs={"k": k})
