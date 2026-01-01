import streamlit as st
import streamlit.components.v1 as components


from stock_logic import (
    fetch_stock_data,
    add_indicators,
    detect_stage,
    trend_signal,
    build_stock_context
)
from rag_engine import get_vector_db, explain_with_rag

def tradingview_chart(symbol):
    html = f"""
    <!-- TradingView Widget BEGIN -->
    <div class="tradingview-widget-container">
      <div id="tradingview_chart"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
      <script type="text/javascript">
      new TradingView.widget(
      {{
        "width": "100%",
        "height": 500,
        "symbol": "{symbol}",
        "interval": "D",
        "timezone": "Asia/Kolkata",
        "theme": "light",
        "style": "1",
        "locale": "en",
        "toolbar_bg": "#f1f3f6",
        "enable_publishing": false,
        "allow_symbol_change": true,
        "hide_side_toolbar": false,
        "studies": [
          "MASimple@tv-basicstudies"
        ],
        "container_id": "tradingview_chart"
      }}
      );
      </script>
    </div>
    <!-- TradingView Widget END -->
    """
    components.html(html, height=520)


st.title("📈 AI Stock Analyst (Minervini Method)")

# Init vector DB ONCE
if "vectordb" not in st.session_state:
    with st.spinner("Loading Minervini knowledge base..."):
        st.session_state.vectordb = get_vector_db()


symbol = st.text_input("Enter Stock Symbol (e.g. TCS, AAPL)")
if symbol:
    st.subheader("📊 Price Chart")
    tradingview_chart(symbol)


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
    
import streamlit as st
import streamlit.components.v1 as components