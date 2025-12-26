from langchain_core.prompts import ChatPromptTemplate

MINERVINI_PROMPT = ChatPromptTemplate.from_messages([
    ("system", 
     "You are a stock market analyst strictly following Mark Minervini methodology."),
    ("human", 
     "Stock data:\n{stock_context}\n\nMinervini rules:\n{rag_context}\n\nQuestion:\n{question}")
])
