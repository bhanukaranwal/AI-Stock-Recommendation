import os
import json
from kiteconnect import KiteConnect, KiteTicker
from config import ZERODHA_API_KEY, ZERODHA_API_SECRET

TOKEN_FILE = "zerodha_access_token.json"

kite = KiteConnect(api_key=ZERODHA_API_KEY)

last_order_signal = {}

def save_access_token(token_data):
    with open(TOKEN_FILE, "w") as f:
        json.dump(token_data, f)

def load_access_token():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            return json.load(f)
    return None

def set_access_token_from_file():
    token_data = load_access_token()
    if token_data and "access_token" in token_data:
        kite.set_access_token(token_data["access_token"])
        return True
    return False

def generate_session(request_token):
    try:
        data = kite.generate_session(request_token, api_secret=ZERODHA_API_SECRET)
        access_token = data["access_token"]
        kite.set_access_token(access_token)
        save_access_token(data)
        print("[INFO] Zerodha session generated and access token saved.")
        return access_token
    except Exception as e:
        print(f"[ERROR] Failed to generate session: {e}")
        raise

def place_order(ticker, side, quantity, product="MIS", order_type="MARKET", exchange="NSE"):
    try:
        transaction_type = kite.TRANSACTION_TYPE_BUY if side.lower() == "buy" else kite.TRANSACTION_TYPE_SELL
        order_id = kite.place_order(
            tradingsymbol=ticker,
            exchange=exchange,
            transaction_type=transaction_type,
            quantity=quantity,
            product=product,
            order_type=order_type,
            variety=kite.VARIETY_REGULAR,
            validity=kite.VALIDITY_DAY
        )
        print(f"[TRADE EXECUTED] {side.upper()} {quantity} shares of {ticker} | Order ID: {order_id}")
        return order_id
    except Exception as e:
        print(f"[ERROR] Order placement failed for {ticker}: {e}")
        return None

def fetch_orders():
    try:
        return kite.orders()
    except Exception as e:
        print(f"[ERROR] Failed to fetch orders: {e}")
        return []

def fetch_positions():
    try:
        return kite.positions()
    except Exception as e:
        print(f"[ERROR] Failed to fetch positions: {e}")
        return {}

def get_instrument_token(symbol, exchange="NSE"):
    try:
        instruments = kite.instruments(exchange)
        for inst in instruments:
            if inst["tradingsymbol"] == symbol:
                return inst["instrument_token"]
    except Exception as e:
        print(f"[ERROR] Fetching instrument token failed: {e}")
    return None

def can_place_order(ticker, signal):
    last_signal = last_order_signal.get(ticker)
    return last_signal != signal

def record_order(ticker, signal):
    last_order_signal[ticker] = signal

def auto_place_order(ticker, signal, shares):
    if can_place_order(ticker, signal):
        side = "buy" if signal == "BUY" else "sell"
        order_id = place_order(ticker, side, shares)
        if order_id:
            record_order(ticker, signal)
            return order_id
    else:
        print(f"[INFO] Already placed order for {ticker} signal {signal}. Skipping.")
    return None

def start_live_feed(instrument_tokens, on_ticks, on_connect=None, on_close=None):
    token_data = load_access_token()
    if not token_data or "access_token" not in token_data:
        raise Exception("Access token required — generate Zerodha session first.")

    access_token = token_data["access_token"]
    kws = KiteTicker(ZERODHA_API_KEY, access_token)

    def _on_connect(ws, response):
        print("[WS] Connected")
        ws.subscribe(instrument_tokens)
        ws.set_mode(ws.MODE_FULL, instrument_tokens)
        if on_connect:
            on_connect(ws, response)

    def _on_ticks(ws, ticks):
        if on_ticks:
            on_ticks(ws, ticks)

    def _on_close(ws, code, reason):
        print(f"[WS] Closed: {code}, {reason}")
        if on_close:
            on_close(ws, code, reason)

    kws.on_ticks = _on_ticks
    kws.on_connect = _on_connect
    kws.on_close = _on_close

    kws.connect(threaded=True)
    return kws

if not set_access_token_from_file():
    print("[WARNING] Zerodha access token not loaded yet. Generate session using request token.")
