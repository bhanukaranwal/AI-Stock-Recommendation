# Replace placeholder strings with your actual keys/secrets before running

REFRESH_INTERVAL = 5           # Minutes between live data refreshes
DEFAULT_CAPITAL = 10000        # Starting capital in USD/INR
RISK_TOLERANCE = "medium"      # "conservative", "medium", "aggressive"
DEFAULT_MODELS = ["RandomForest", "XGBoost"]  # ML models to load/use

STOP_LOSS = 0.05               # 5% stop-loss threshold
TAKE_PROFIT = 0.1              # 10% take-profit threshold

NEWS_API_KEY = "YOUR_NEWSAPI_KEY"
TWITTER_BEARER_TOKEN = "YOUR_TWITTER_BEARER_TOKEN"  # Optional

ZERODHA_API_KEY = "your_zerodha_api_key"
ZERODHA_API_SECRET = "your_zerodha_api_secret"
