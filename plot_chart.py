import plotly.graph_objects as go
from plotly.subplots import make_subplots

def plot_stock_chart(df, symbol):
    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        row_heights=[0.7, 0.3]
    )

    # --- Candlestick ---
    fig.add_trace(
        go.Candlestick(
            x=df.index,
            open=df["Open"],
            high=df["High"],
            low=df["Low"],
            close=df["Close"],
            name="Price"
        ),
        row=1, col=1
    )

    # --- Moving Averages ---
    fig.add_trace(
        go.Scatter(x=df.index, y=df["DMA50"], name="DMA 50", line=dict(color="blue", width=1)),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=df.index, y=df["DMA150"], name="DMA 150", line=dict(color="orange", width=2)),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=df.index, y=df["DMA200"], name="DMA 200", line=dict(color="red", width=2)),
        row=1, col=1
    )
        # --- Volume Bars ---
    volume_colors = [
        "green" if df["Close"].iloc[i] >= df["Close"].iloc[i - 1] else "red"
        for i in range(1, len(df))
    ]
    volume_colors.insert(0, "green")

    fig.add_trace(
        go.Bar(
            x=df.index,
            y=df["Volume"],
            marker_color=volume_colors,
            name="Volume"
        ),
        row=2, col=1
    )

    fig.update_layout(
        title=f"{symbol} – Price & Moving Averages",
        xaxis_rangeslider_visible=False,
        height=650,
        legend=dict(orientation="h", yanchor="bottom", y=1.02)
    )
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

    return fig
