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

symbol = st.text_input("Enter Stock Symbol (e.g. TCS, AAPL)")

if symbol:
    df = fetch_stock_data(symbol)
    df = add_indicators(df)

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
    