from langchain_core.messages import HumanMessage
import streamlit as st
from plot_chart import plot_stock_chart
from stock_logic import (
    fetch_stock_data,
    add_indicators,
    detect_stage,
    trend_signal,
    build_stock_context
)
from rag_engine import get_vector_db


st.title("📈 AI Stock Analyst (Minervini Method)")

# Init vector DB ONCE
if "vectordb" not in st.session_state:
    with st.spinner("Loading Minervini knowledge base..."):
        st.session_state.vectordb = get_vector_db()


def normalize_yfinance_symbol(symbol, market):
    symbol = symbol.upper().strip()

    if market == "NSE":
        return f"{symbol}.NS"
    elif market == "BSE":
        return f"{symbol}.BO"
    elif market == "US":
        return symbol
    
market = st.selectbox(
    "Select Market",
    ["NSE", "BSE", "US"]
)

symbol = st.text_input("Enter Stock Symbol (e.g. TCS, AAPL)")

if symbol:
    yf_symbol = normalize_yfinance_symbol(symbol,market)
    df = fetch_stock_data(yf_symbol)
    df = add_indicators(df)
    st.subheader("📊 Price Chart")
    fig = plot_stock_chart(df, yf_symbol)
    st.plotly_chart(fig, use_container_width=True)
    risk_pct = 8
    st.warning(
        f"⚠️ Risk View: Initial stop-loss must  not exceed ~{risk_pct}% below entry price. "
        "Minervini advises exiting quickly if a stock violates key moving averages."
    )


    stage = detect_stage(df)
    trend = trend_signal(stage)

    latest = df.iloc[-1]

    st.success(f"Stage: {stage}")
    st.info(f"Trend: {trend}")

    stock_context = build_stock_context(
        symbol, stage, trend, latest
    )
    if "stock_context" not in st.session_state:
        st.session_state.stock_context = stock_context

    # init LLM agent with current context
    from chat_agent import create_stock_chat_agent
    if "current_symbol" not in st.session_state or st.session_state.current_symbol != yf_symbol:
        st.session_state.current_symbol = yf_symbol
        st.session_state.agent = create_stock_chat_agent(st.session_state.stock_context, st.session_state.vectordb)

    question = st.text_input(
        "Ask about this stock (Minervini style)",
        "Is this stock in a proper buyable stage?"
    )

    if "thread_id" not in st.session_state:
        st.session_state.thread_id = f"{yf_symbol}_chat"
    if question:
        response = st.session_state.agent.invoke(
            {
                "messages": [
                    HumanMessage(content=question)
                ]
            },
            {
                "configurable": {
                    "thread_id": f"{yf_symbol}_chat"
                }
            }
        )

        st.write(response["messages"][-1].content)
