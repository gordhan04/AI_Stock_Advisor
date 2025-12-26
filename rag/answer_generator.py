from config.prompts import MINERVINI_PROMPT
from rag.llm import get_llm

def generate_answer(question, stock_context, retriever):
    llm = get_llm()

    docs = retriever.invoke(question)
    rag_context = "\n\n".join(doc.page_content for doc in docs)

    messages = MINERVINI_PROMPT.invoke({
        "stock_context": stock_context,
        "rag_context": rag_context,
        "question": question
    })

    response = llm.invoke(messages)
    return response.content
