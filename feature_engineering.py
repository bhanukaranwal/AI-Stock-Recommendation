import ta

def add_technical_indicators(df):
    df["RSI"] = ta.momentum.RSIIndicator(df["Close"], window=14).rsi()
    df["MACD"] = ta.trend.MACD(df["Close"]).macd()
    df["SMA_50"] = df["Close"].rolling(window=50).mean()
    df["SMA_200"] = df["Close"].rolling(window=200).mean()
    df["EMA_20"] = ta.trend.EMAIndicator(df["Close"], window=20).ema_indicator()
    df["EMA_50"] = ta.trend.EMAIndicator(df["Close"], window=50).ema_indicator()
    df["ATR"] = ta.volatility.AverageTrueRange(df["High"], df["Low"], df["Close"]).average_true_range()
    return df.dropna()

def create_labels(df):
    df["Tomorrow_Close"] = df["Close"].shift(-1)
    df["Target"] = (df["Tomorrow_Close"] > df["Close"]).astype(int)
    return df.dropna()
