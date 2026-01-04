"""
Stock Chart Plotting Module
Creates interactive Plotly charts for stock price analysis with technical indicators.
"""

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def plot_stock_chart(df: pd.DataFrame, symbol: str) -> go.Figure:
    """
    Create an interactive stock chart with price, moving averages, and volume.

    Args:
        df: DataFrame containing OHLCV data and technical indicators
        symbol: Stock symbol for chart title

    Returns:
        Plotly figure with candlestick chart, moving averages, and volume
    """
    # Create subplot figure
    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        row_heights=[0.7, 0.3],
        subplot_titles=("Price & Moving Averages", "Volume")
    )

    # Add candlestick chart
    fig.add_trace(
        go.Candlestick(
            x=df.index,
            open=df["Open"],
            high=df["High"],
            low=df["Low"],
            close=df["Close"],
            name="Price",
            increasing_line_color="green",
            decreasing_line_color="red"
        ),
        row=1, col=1
    )

    # Add moving averages
    moving_averages = [
        ("DMA50", "DMA 50", "blue", 1),
        ("DMA150", "DMA 150", "orange", 2),
        ("DMA200", "DMA 200", "red", 2),
    ]

    for col, name, color, width in moving_averages:
        if col in df.columns:
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df[col],
                    name=name,
                    line=dict(color=color, width=width)
                ),
                row=1, col=1
            )

    # Add volume bars with color coding
    volume_colors = [
        "green" if df["Close"].iloc[i] >= df["Close"].iloc[i - 1] else "red"
        for i in range(1, len(df))
    ]
    volume_colors.insert(0, "green")  # First bar is green by default

    fig.add_trace(
        go.Bar(
            x=df.index,
            y=df["Volume"],
            marker_color=volume_colors,
            name="Volume",
            showlegend=False
        ),
        row=2, col=1
    )

    # Highlight Stage 2 periods (price > DMA150 > DMA200)
    _add_stage2_highlights(df, fig)

    # Update layout
    fig.update_layout(
        title=f"{symbol} – Price & Moving Averages",
        xaxis_rangeslider_visible=False,
        height=650,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        ),
        yaxis2_title="Volume"
    )

    # Update y-axes titles
    fig.update_yaxes(title_text="Price", row=1, col=1)
    fig.update_yaxes(title_text="Volume", row=2, col=1)

    return fig


def _add_stage2_highlights(df: pd.DataFrame, fig: go.Figure) -> None:
    """
    Add background highlights for Stage 2 periods in the Minervini trend template.

    Stage 2 is when price > DMA150 > DMA200.

    Args:
        df: DataFrame with price and moving average data
        fig: Plotly figure to add highlights to
    """
    if not all(col in df.columns for col in ["Close", "DMA150", "DMA200"]):
        return

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
                line_width=0,
                annotation_text="Stage 2",
                annotation_position="top left"
            )
            in_zone = False

    # Handle case where still in stage 2 at the end
    if in_zone:
        fig.add_vrect(
            x0=start_date,
            x1=df.index[-1],
            fillcolor="rgba(0, 255, 0, 0.12)",
            line_width=0,
            annotation_text="Stage 2",
            annotation_position="top left"
        )
