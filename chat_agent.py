"""
Chat Agent for Stock Analysis
Handles AI-powered conversations about stock analysis using Minervini methodology.
"""

from typing import Any

from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import InMemorySaver

from rag_engine import get_rag_context


# Initialize the language model
model = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
    max_tokens=None,
    reasoning_format="parsed",
    timeout=None,
    max_retries=2,
    streaming=True,  # Enable streaming for better response handling
)


def create_stock_chat_agent(stock_context: str, vectordb: Any) -> Any:
    """
    Create a stock analysis chat agent with access to stock data and Minervini knowledge.

    Args:
        stock_context: String containing current stock analysis data
        vectordb: Vector database for retrieving Minervini methodology references

    Returns:
        Configured LangChain agent for stock analysis conversations
    """

    @tool
    def explain_stock_tool(question: str) -> str:
        """
        Tool for explaining stock analysis using Minervini methodology.

        This tool is ALWAYS called for every user question to ensure
        responses are based on proper analysis and methodology.

        Args:
            question: User's question about the stock

        Returns:
            Formatted context string containing stock data and relevant references
        """
        # Retrieve relevant Minervini methodology references
        rag_context = get_rag_context(question, vectordb)

        # Format the complete context for the AI to analyze
        return (
            "You MUST base your answer only on the following context.\n\n"
            f"Stock Data:\n{stock_context}\n\n"
            f"Minervini Reference:\n{rag_context}\n\n"
            f"User Question:\n{question}"
        )

    # Create the agent with strict instructions to always use the tool
    agent = create_agent(
        model,
        tools=[explain_stock_tool],
        checkpointer=InMemorySaver(),
        system_prompt=(
            "You are an expert stock analysis assistant specializing in the Minervini Trend Template.\n\n"
            "CRITICAL INSTRUCTIONS:\n"
            "- For EVERY user question, you MUST call the `explain_stock_tool` tool first\n"
            "- Do NOT answer from memory or general knowledge\n"
            "- Always base your analysis on the provided stock data and Minervini references\n"
            "- Provide clear, actionable insights following Minervini principles\n"
            "- Be concise but comprehensive in your explanations"
        ),
    )

    return agent