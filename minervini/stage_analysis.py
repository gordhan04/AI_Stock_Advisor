# Minervini Stock Stage Analysis

def detect_stage(df):
    latest = df.iloc[-1]

    if (
        latest["Close"] > latest["DMA150"] > latest["DMA200"]
    ):
        return "Stage 2 (Advancing)"
    
    if (
        latest["Close"] < latest["DMA150"] < latest["DMA200"]
    ):
        return "Stage 4 (Declining)"
    
    return "Stage 1 or 3 (Base / Topping)"

# stage = detect_stage(df)
