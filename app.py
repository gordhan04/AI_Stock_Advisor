"""
AI Stock Analyst using Minervini Method
A Streamlit application for stock analysis based on Mark Minervini's trend template.
"""

from langchain_core.messages import HumanMessage
import streamlit as st
import time

from plot_chart import plot_stock_chart
from stock_logic import (
    fetch_stock_data,
    add_indicators,
    detect_stage,
    trend_signal,
    build_stock_context
)
from rag_engine import get_vector_db


# Constants
DEFAULT_RISK_PCT = 8


# Page configuration
st.set_page_config(
    page_title="AI Stock Analyst",
    page_icon="📈",
    layout="wide"
)

st.title("📈 AI Stock Analyst (Minervini Method)")


def normalize_yfinance_symbol(symbol: str, market: str) -> str:
    """
    Normalize stock symbol for Yahoo Finance based on market.

    Args:
        symbol: Stock ticker symbol
        market: Market (NSE, BSE, US)

    Returns:
        Normalized symbol for yfinance
    """
    symbol = symbol.upper().strip()

    market_suffixes = {
        "NSE": ".NS",
        "BSE": ".BO",
        "US": ""
    }

    return f"{symbol}{market_suffixes.get(market, '')}"


def clear_chat_history() -> None:
    """Clear the chat history for the current stock."""
    if "thread_id" in st.session_state:
        # Reset thread to start new conversation
        current_symbol = st.session_state.get("current_symbol", "")
        st.session_state.thread_id = f"{current_symbol}_chat_{int(time.time())}"
        st.success("Chat history cleared!")


# Initialize vector DB once per session
if "vectordb" not in st.session_state:
    with st.spinner("Loading Minervini knowledge base..."):
        st.session_state.vectordb = get_vector_db()


# Sidebar for inputs
with st.sidebar:
    st.header("Stock Selection")

    market = st.selectbox(
        "Select Market",
        ["NSE", "BSE", "US"],
        help="Choose the stock market for analysis"
    )

    symbol = st.text_input(
        "Enter Stock Symbol",
        placeholder="e.g. TCS, AAPL, RELIANCE",
        help="Enter the stock ticker symbol"
    ).strip()

    if symbol:
        st.markdown("---")
        st.subheader("Chat Controls")
        if st.button("🗑️ Clear Chat History", help="Start a new conversation"):
            clear_chat_history()


# Main content area
if symbol:
    try:
        # Normalize symbol for yfinance
        yf_symbol = normalize_yfinance_symbol(symbol, market)

        # Fetch and process stock data
        with st.spinner(f"Fetching data for {symbol}..."):
            df = fetch_stock_data(yf_symbol)

        if df is None or df.empty:
            st.error(f"❌ Could not fetch data for symbol '{symbol}'. Please check the symbol and try again.")
            st.stop()

        # Add technical indicators
        df = add_indicators(df)

        # Display price chart
        st.subheader("📊 Price Chart")
        fig = plot_stock_chart(df, yf_symbol)
        st.plotly_chart(fig, use_container_width=True)

        # Risk warning
        st.warning(
            f"⚠️ **Risk Management**: Initial stop-loss should not exceed ~{DEFAULT_RISK_PCT}% below entry price. "
            "Minervini advises exiting quickly if a stock violates key moving averages."
        )

        # Analyze stock stage and trend
        stage = detect_stage(df)
        trend = trend_signal(stage)
        latest = df.iloc[-1]

        # Display analysis results
        col1, col2 = st.columns(2)
        with col1:
            st.success(f"**Stage**: {stage}")
        with col2:
            st.info(f"**Trend**: {trend}")

        # Build stock context for AI analysis
        stock_context = build_stock_context(symbol, stage, trend, latest)
        st.session_state.stock_context = stock_context

        # Initialize AI agent with current stock context
        from chat_agent import create_stock_chat_agent
        if ("current_symbol" not in st.session_state or
            st.session_state.current_symbol != yf_symbol):
            st.session_state.current_symbol = yf_symbol
            with st.spinner("Initializing AI analyst..."):
                st.session_state.agent = create_stock_chat_agent(
                    st.session_state.stock_context,
                    st.session_state.vectordb
                )

        # Chat interface
        st.subheader("🤖 AI Analyst Chat")
        question = st.text_input(
            "Ask about this stock (Minervini style)",
            placeholder="e.g. Is this stock in a proper buyable stage?",
            help="Ask questions about the stock's Minervini analysis"
        )

        # Set thread ID for conversation continuity
        thread_id = f"{yf_symbol}_chat"
        st.session_state.thread_id = thread_id

        if question:
            with st.spinner("Analyzing..."):
                response = st.session_state.agent.invoke(
                    {
                        "messages": [HumanMessage(content=question)]
                    },
                    {
                        "configurable": {"thread_id": thread_id}
                    }
                )

            # Display response
            st.write("**AI Analyst:**")
            st.write(response["messages"][-1].content)

    except Exception as e:
        st.error(f"❌ An error occurred while analyzing {symbol}: {str(e)}")
        st.info("💡 Please try again or contact support if the issue persists.")

else:
    # Welcome message when no symbol is entered
    st.info("👋 Welcome! Please select a market and enter a stock symbol in the sidebar to begin analysis.")
    st.markdown("""
    ### How to use:
    1. **Select Market**: Choose NSE, BSE, or US
    2. **Enter Symbol**: Input stock ticker (e.g., TCS, AAPL, RELIANCE)
    3. **View Analysis**: See technical charts and Minervini stage
    4. **Ask Questions**: Chat with AI analyst about the stock
    5. **Clear Chat**: Use sidebar button to reset conversation

    ### Features:
    - 📊 Interactive technical charts with moving averages
    - 🎯 Minervini trend template analysis
    - 🤖 AI-powered stock insights
    - 📈 Multi-market support
    - 📚 Knowledge base from Minervini methodology
    """)
