import pandas as pd

def rank_stocks(results_df):
    results_df["Rank"] = results_df["Predicted_Return %"].rank(ascending=False)
    return results_df.sort_values("Rank")

def allocate_portfolio(results_df, capital=10000):
    ranked = rank_stocks(results_df)
    allocation = capital / len(ranked) if len(ranked) > 0 else 0
    ranked["Allocation_$"] = allocation
    ranked["Shares"] = (ranked["Allocation_$"] / ranked["Last_Close"]).apply(lambda x: max(1, int(x)))
    return ranked
