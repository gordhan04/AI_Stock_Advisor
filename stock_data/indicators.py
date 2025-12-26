# Technical Indicators

def add_indicators(df):
    df["DMA50"] = df["Close"].rolling(50).mean()
    df["DMA150"] = df["Close"].rolling(150).mean()
    df["DMA200"] = df["Close"].rolling(200).mean()
    return df
