# Bullish Bearish Decision

def trend_signal(stage):
    if stage.startswith("Stage 2"):
        return "Bullish"
    elif stage.startswith("Stage 4"):
        return "Bearish"
    return "Neutral"
