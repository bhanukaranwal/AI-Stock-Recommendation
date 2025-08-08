import streamlit as st
import pandas as pd
import numpy as np
from collections import deque
from datetime import datetime
from data_fetcher import get_stock_data, get_stock_news
from feature_engineering import add_technical_indicators, create_labels
from models import train_random_forest, predict_signal
from sentiment import compute_sentiment
from backtest import backtest_strategy
from portfolio import allocate_portfolio
from broker_api import (
    kite, generate_session, fetch_orders, fetch_positions, place_order,
    set_access_token_from_file, get_instrument_token, start_live_feed,
    auto_place_order
)
from risk_management import RiskManager
from config import DEFAULT_CAPITAL, STOP_LOSS, TAKE_PROFIT
import threading
import time

# Configure Page
st.set_page_config(page_title="🚀 AI Stock Trading Bot with Zerodha", layout="wide")
st.title("🚀 Advanced AI Stock Recommendation & Auto-Trading Platform")

# -- Zerodha Authentication --
if "zerodha_authenticated" not in st.session_state:
    st.session_state.zerodha_authenticated = False

if not st.session_state.zerodha_authenticated:
    # Try load existing access token silently
    if set_access_token_from_file():
        st.session_state.zerodha_authenticated = True

if not st.session_state.zerodha_authenticated:
    st.sidebar.header("📌 Zerodha Login")
    st.sidebar.write("1. Click this login URL and sign in with Zerodha credentials:")
    st.sidebar.code(kite.login_url())
    request_token = st.sidebar.text_input("Enter Request Token (from URL redirect after login):")
    if st.sidebar.button("Generate Session"):
        if request_token:
            try:
                generate_session(request_token)
                st.session_state.zerodha_authenticated = True
                st.sidebar.success("✅ Authenticated successfully!")
            except Exception as e:
                st.sidebar.error(f"Authentication failed: {e}")
        else:
            st.sidebar.warning("Please enter the request token from Zerodha login redirect.")
else:
    st.sidebar.success("✅ Zerodha session active")

# -- User Inputs --
tickers = st.multiselect(
    "Select Stock Tickers",
    ["AAPL", "MSFT", "GOOGL", "TSLA", "AMZN", "META", "NVDA"],
    default=["AAPL", "MSFT"]
)
capital = st.sidebar.number_input("Starting Capital ($ or INR)", value=DEFAULT_CAPITAL)

if not tickers:
    st.warning("Please select at least one ticker to continue.")
    st.stop()

# -- Setup ticker-to-token mappings --
if st.session_state.zerodha_authenticated:
    token_to_ticker = {}
    ticker_to_token = {}
    for t in tickers:
        try:
            token = get_instrument_token(t)
            if token:
                token_to_ticker[token] = t
                ticker_to_token[t] = token
        except Exception:
            st.error(f"Failed to get instrument token for {t}")

    # Initialize persistent session states
    if "price_histories" not in st.session_state:
        st.session_state.price_histories = {t: deque(maxlen=250) for t in tickers}
    if "live_signals" not in st.session_state:
        st.session_state.live_signals = {t: "N/A" for t in tickers}
    if "live_prices" not in st.session_state:
        st.session_state.live_prices = {t: 0.0 for t in tickers}
    if "portfolio_allocation" not in st.session_state:
        st.session_state.portfolio_allocation = {}

    risk_manager = RiskManager(capital, stop_loss_pct=STOP_LOSS, take_profit_pct=TAKE_PROFIT)

    # Train ML model (Random Forest example on first ticker)
    if "rf_model" not in st.session_state:
        with st.spinner(f"Training model on {tickers[0]} data..."):
            df_train = get_stock_data(tickers[0])
            df_train = add_technical_indicators(df_train)
            df_train = create_labels(df_train)
            model_rf, accuracy = train_random_forest(df_train)
            st.success(f"Random Forest model trained with accuracy: {accuracy:.2%}")
            st.session_state.rf_model = model_rf

    model_rf = st.session_state.rf_model

    # Function to update price history and generate signals
    def update_price_and_predict(ticker, price):
        st.session_state.price_histories[ticker].append(price)
        prices_list = list(st.session_state.price_histories[ticker])

        if len(prices_list) < 50:
            # Need minimum data for reliable indicators
            return

        df_temp = pd.DataFrame({
            "Open": prices_list,
            "High": prices_list,
            "Low": prices_list,
            "Close": prices_list
        })

        df_temp = add_technical_indicators(df_temp)
        df_temp = create_labels(df_temp)
        if df_temp.empty:
            return

        latest_feat = df_temp.iloc[-1:]
        new_signal = predict_signal(model_rf, latest_feat)
        old_signal = st.session_state.live_signals.get(ticker, "N/A")

        # Only trade if signal changed and risk manager allows trade now
        if new_signal != old_signal and risk_manager.can_trade(ticker):
            # Calculate shares based on portfolio allocation & latest price
            allocation = st.session_state.portfolio_allocation.get(ticker, capital / len(tickers))
            shares = max(1, int(allocation / latest_feat["Close"].values[0]))

            # Place order via Zerodha
            order_id = auto_place_order(ticker, new_signal, shares)
            if order_id:
                st.session_state.live_signals[ticker] = new_signal
                risk_manager.update_trade_time(ticker)

        st.session_state.live_prices[ticker] = price

    # Zerodha live tick event handler
    def on_live_ticks(ws, ticks):
        for tick in ticks:
            token = tick["instrument_token"]
            price = tick["last_price"]
            tkr = token_to_ticker.get(token)
            if tkr:
                update_price_and_predict(tkr, price)

    # Start WebSocket feed once
    if "ws_feed_started" not in st.session_state:
        st.session_state.ws_feed_started = True
        start_live_feed(list(token_to_ticker.keys()), on_live_ticks)
        st.success("📡 Live Zerodha market data streaming started.")

    # Portfolio allocation based on backtested returns
    st.subheader("📈 Portfolio Allocation & Backtest")
    res = []
    with st.spinner("Calculating portfolio allocation and backtesting..."):
        for ticker in tickers:
            df = get_stock_data(ticker)
            df = add_technical_indicators(df)
            df = create_labels(df)
            metrics = backtest_strategy(df, model_rf)
            last_close = df["Close"].iloc[-1]
            predicted_return = metrics.get("Total Return %", 0)
            res.append({"Ticker": ticker, "Last_Close": last_close, "Predicted_Return %": predicted_return})

        results_df = pd.DataFrame(res)
        portfolio_df = allocate_portfolio(results_df, capital)
        st.session_state.portfolio_allocation = dict(zip(portfolio_df["Ticker"], portfolio_df["Allocation_$"]))
        st.dataframe(portfolio_df[["Ticker", "Predicted_Return %", "Allocation_$", "Shares"]])

    # Live prices & signals display
    st.subheader("🌐 Live Prices & Signals")
    live_data = []
    for t in tickers:
        live_data.append({
            "Ticker": t,
            "Live Price": round(st.session_state.live_prices.get(t, 0), 2),
            "Signal": st.session_state.live_signals.get(t, "N/A")
        })
    st.table(pd.DataFrame(live_data))

    # Show Zerodha positions & orders
    st.subheader("📋 Current Zerodha Positions & Recent Orders")
    positions = fetch_positions()
    if positions and positions.get("net"):
        st.write("Open Positions:")
        st.dataframe(pd.DataFrame(positions["net"]))
    else:
        st.write("No open positions or data unavailable.")

    orders = fetch_orders()
    if orders:
        st.write("Recent Orders:")
        st.dataframe(pd.DataFrame(orders))
    else:
        st.write("No recent orders or data unavailable.")

else:
    st.info("Please authenticate with Zerodha to enable live trading.")

