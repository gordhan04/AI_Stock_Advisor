import streamlit as st
from plot_chart import plot_stock_chart
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

symbol = st.text_input("Enter Stock Symbol (e.g. TCS, AAPL)")

if symbol:
    yf_symbol = normalize_yfinance_symbol(symbol,market)
    df = fetch_stock_data(yf_symbol)
    df = add_indicators(df)
    st.subheader("📊 Price Chart")
    fig = plot_stock_chart(df, yf_symbol)
        # --- Stage-2 Highlight Zones ---
    stage2 = (df["Close"] > df["DMA150"]) & (df["DMA150"] > df["DMA200"])

    in_zone = False
    start_date = None

    for date, is_stage2 in stage2.items():
        if is_stage2 and not in_zone:
            start_date = date
            in_zone = True
        elif not is_stage2 and in_zone:
            fig.add_vrect(
                x0=start_date,
                x1=date,
                fillcolor="rgba(0, 255, 0, 0.12)",
                line_width=0
            )
            in_zone = False

    # If still in stage-2 at end
    if in_zone:
        fig.add_vrect(
            x0=start_date,
            x1=df.index[-1],
            fillcolor="rgba(0, 255, 0, 0.12)",
            line_width=0
        )
    st.plotly_chart(fig, use_container_width=True)

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

