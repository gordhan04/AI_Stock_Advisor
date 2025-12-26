# Stock Data Loading


import yfinance as yf

def fetch_stock_data(symbol):
    stock = yf.Ticker(symbol)
    df = stock.history(period="3y")
    return df


data = fetch_stock_data("MSFT")
