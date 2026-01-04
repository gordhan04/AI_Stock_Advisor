from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage

from rag_engine import get_rag_context

model = ChatGroq(
        model="openai/gpt-oss-20b",
        temperature=0,
        max_tokens=None,
        reasoning_format="parsed",
        timeout=None,
        max_retries=2,
        streaming=True,
    )

def create_stock_chat_agent(stock_context, vectordb):
    # We will use Tool for explanation only(not for logic)
    @tool
    def explain_stock_tool(question: str) -> str:
        """ 
        ALWAYS use this tool to answer.
        Explains stock analysis using Minervini methodology with retrieved context.
        """
        rag_context = get_rag_context(question, vectordb)

        return (
            "You MUST base your answer only on the following context.\n\n"
            f"Stock Data:\n{stock_context}\n\n"
            f"Minervini Reference:\n{rag_context}\n\n"
            f"User Question:\n{question}"
        )

    agent = create_agent(
        model,
        tools =[explain_stock_tool],
        checkpointer=InMemorySaver(),
        system_prompt=(
            "You are a stock analysis assistant.\n"
            "For EVERY user question, you MUST call the tool "
            "`explain_stock_tool` before responding.\n"
            "Do NOT answer from memory. Do NOT skip the tool."
        )
    )
    return agent