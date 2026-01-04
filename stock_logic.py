"""
Stock Analysis Logic
Pure financial analysis functions for Minervini trend template implementation.
"""

import pandas as pd
import yfinance as yf


def fetch_stock_data(symbol: str, period: str = "3y") -> pd.DataFrame:
    """
    Fetch historical stock data from Yahoo Finance.

    Args:
        symbol: Stock symbol (e.g., 'AAPL', 'TCS.NS')
        period: Time period for data (default: 3 years)

    Returns:
        DataFrame with OHLCV data

    Raises:
        ValueError: If symbol is invalid or no data available
    """
    try:
        stock = yf.Ticker(symbol)
        df = stock.history(period=period)

        if df.empty:
            raise ValueError(f"No data available for symbol '{symbol}'")

        return df.dropna()

    except Exception as e:
        raise ValueError(f"Failed to fetch data for '{symbol}': {str(e)}")


def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add technical indicators (moving averages) to the DataFrame.

    Args:
        df: DataFrame with price data

    Returns:
        DataFrame with added moving average columns
    """
    df = df.copy()  # Avoid modifying original

    # Calculate moving averages
    df["DMA50"] = df["Close"].rolling(window=50, min_periods=1).mean()
    df["DMA150"] = df["Close"].rolling(window=150, min_periods=1).mean()
    df["DMA200"] = df["Close"].rolling(window=200, min_periods=1).mean()

    return df


def detect_stage(df: pd.DataFrame) -> str:
    """
    Detect the current stage in Minervini's trend template.

    Args:
        df: DataFrame with price and moving average data

    Returns:
        String describing the current stage
    """
    if df.empty:
        return "Unknown (No Data)"

    r = df.iloc[-1]  # Most recent data

    close = r["Close"]
    dma50 = r.get("DMA50", float('inf'))
    dma150 = r.get("DMA150", float('inf'))
    dma200 = r.get("DMA200", float('inf'))

    # Stage 2: Price above all moving averages in proper order
    if close > dma150 > dma200:
        return "Stage 2 (Advancing)"

    # Stage 4: Price below all moving averages
    if close < dma150 < dma200:
        return "Stage 4 (Declining)"

    # Stage 1 or 3: Mixed conditions
    return "Stage 1 or 3 (Base Building / Topping)"


def trend_signal(stage: str) -> str:
    """
    Determine trend signal based on the detected stage.

    Args:
        stage: Stage string from detect_stage()

    Returns:
        Trend signal: "Bullish", "Bearish", or "Neutral"
    """
    if "Stage 2" in stage:
        return "Bullish 📈"
    elif "Stage 4" in stage:
        return "Bearish 📉"
    else:
        return "Neutral ➡️"


def build_stock_context(symbol: str, stage: str, trend: str, row: pd.Series) -> str:
    """
    Build a formatted context string for AI analysis.

    Args:
        symbol: Stock symbol
        stage: Current stage
        trend: Trend signal
        row: Latest data row

    Returns:
        Formatted context string
    """
    return f"""
Stock: {symbol}
Close Price: ${row['Close']:.2f}

Technical Indicators:
- 50 DMA: ${row.get('DMA50', 'N/A'):.2f}
- 150 DMA: ${row.get('DMA150', 'N/A'):.2f}
- 200 DMA: ${row.get('DMA200', 'N/A'):.2f}

Minervini Analysis:
- Stage: {stage}
- Trend: {trend}
""".strip()
