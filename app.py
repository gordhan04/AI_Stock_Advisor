# Main Streamlit App Simple Streamlit UI

import streamlit as st
from stock_data.fetcher import fetch_stock_data
from stock_data.indicators import add_indicators
from minervini.stage_analysis import detect_stage

symbol = st.text_input("Enter stock symbol")

if symbol:
    df = fetch_stock_data(symbol)
    df = add_indicators(df)
    stage = detect_stage(df)

    st.write("Stage:", stage)
