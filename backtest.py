import numpy as np

def backtest_strategy(df, model):
    features = ["RSI", "MACD", "SMA_50", "SMA_200", "EMA_20", "EMA_50", "ATR"]
    returns = []
    for i in range(len(df) - 1):
        pred = model.predict(df[features].iloc[i].values.reshape(1, -1))[0]
        if pred == 1:
            ret = (df["Close"].iloc[i + 1] - df["Close"].iloc[i]) / df["Close"].iloc[i]
            returns.append(ret)
        else:
            returns.append(0)
    if returns:
        win_rate = sum([1 for r in returns if r > 0]) / len(returns)
        cagr = (1 + np.mean(returns)) ** 252 - 1
        cumulative = np.cumprod([1 + r for r in returns])
        max_dd = np.min(cumulative / np.maximum.accumulate(cumulative) - 1)
        total_return = sum(returns)
        return {
            "Total Return %": total_return * 100,
            "Win Rate %": win_rate * 100,
            "CAGR %": cagr * 100,
            "MaxDrawdown %": max_dd * 100,
        }
    return {}
