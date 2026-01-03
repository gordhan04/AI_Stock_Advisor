import streamlit as st

from stock_logic import (
    fetch_stock_data,
    add_indicators,
    detect_stage,
    trend_signal,
    build_stock_context
)
from rag_engine import get_vector_db, explain_with_rag

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

import plotly.graph_objects as go

def plot_stock_chart(df, symbol):
    fig = go.Figure(
        data=[
            go.Candlestick(
                x=df.index,
                open=df["Open"],
                high=df["High"],
                low=df["Low"],
                close=df["Close"],
                name="Price"
            )
        ]
    )

    fig.update_layout(
        title=f"{symbol} Price Chart",
        xaxis_title="Date",
        yaxis_title="Price",
        height=520,
        xaxis_rangeslider_visible=False
    )

    st.plotly_chart(fig, use_container_width=True)

symbol = st.text_input("Enter Stock Symbol (e.g. TCS, AAPL)")

if symbol:
    yf_symbol = normalize_yfinance_symbol(symbol,market)
    df = fetch_stock_data(yf_symbol)
    df = add_indicators(df)
    st.subheader("📊 Price Chart")
    plot_stock_chart(df, yf_symbol)
    stage = detect_stage(df)
    trend = trend_signal(stage)

    latest = df.iloc[-1]

    st.success(f"Stage: {stage}")
    st.info(f"Trend: {trend}")

    stock_context = build_stock_context(
        symbol, stage, trend, latest
    )

    question = st.text_input(
        "Ask about this stock (Minervini style)",
        "Is this stock in a proper buyable stage?"
    )

    if question:
        answer = explain_with_rag(
            question,
            stock_context,
            st.session_state.vectordb
        )

        st.markdown("### 📘 Explanation")
        st.write(answer)
    