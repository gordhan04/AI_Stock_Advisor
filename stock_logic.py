# Pure finance logic (NO AI)
import yfinance as yf
import pandas as pd

def fetch_stock_data(symbol):
    stock = yf.Ticker(symbol)
    df = stock.history(period="3y")
    return df.dropna()

def add_indicators(df):
    df["DMA50"] = df["Close"].rolling(50).mean()
    df["DMA150"] = df["Close"].rolling(150).mean()
    df["DMA200"] = df["Close"].rolling(200).mean()
    return df

def detect_stage(df):
    r = df.iloc[-1]

    if r["Close"] > r["DMA150"] > r["DMA200"]:
        return "Stage 2 (Advancing)"
    if r["Close"] < r["DMA150"] < r["DMA200"]:
        return "Stage 4 (Declining)"
    return "Stage 1 or 3 (Base / Topping)"

def trend_signal(stage):
    if stage.startswith("Stage 2"):
        return "Bullish"
    if stage.startswith("Stage 4"):
        return "Bearish"
    return "Neutral"

def build_stock_context(symbol, stage, trend, row):
    return f"""
Stock: {symbol}
Close Price: {row['Close']:.2f}

50 DMA: {row['DMA50']:.2f}
150 DMA: {row['DMA150']:.2f}
200 DMA: {row['DMA200']:.2f}

Stage: {stage}
Trend: {trend}
"""
