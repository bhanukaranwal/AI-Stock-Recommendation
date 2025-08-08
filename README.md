# Stock AI Trader: Advanced AI-Powered Stock Recommendation & Automated Trading System

Welcome to **Stock AI Trader**, a cutting-edge Python project that combines machine learning, deep learning, real-time market data, sentiment analysis, and Zerodha brokerage integration to deliver a **fully automated, intelligent stock trading platform**. This system empowers you to analyze, predict, and trade stocks with minimal manual intervention via a user-friendly **interactive Streamlit dashboard**.

---

## 🔥 Key Features

- **Multi-Stock Support:** Select and manage multiple stock tickers simultaneously.
- **Comprehensive Data Sourcing:** Fetch historical stock market data and real-time live ticks via Zerodha WebSocket.
- **Technical Indicator Engineering:** Calculate advanced indicators (RSI, MACD, SMA, EMA, ATR) for powerful feature representation.
- **Multiple AI Models:** Use classical ML models (Random Forest, XGBoost), deep learning (LSTM), and trend forecasting (Prophet) for accurate stock movement predictions.
- **Real-Time Sentiment Analysis:** Incorporate financial news sentiment to enhance decision making.
- **Automated Trading:** Place and manage live market orders through Zerodha Kite Connect API based on AI signals.
- **Advanced Risk Management:** Built-in stop-loss, take-profit, and cooldown controls safeguard capital and reduce overtrading.
- **Backtesting & Portfolio Optimization:** Evaluate strategies historically and allocate funds efficiently to maximize returns.
- **Interactive Streamlit Dashboard:** Visualize live prices, recommendations, portfolio status, positions, and orders, with intuitive controls.
- **Secure Authentication:** Seamlessly authenticate with Zerodha API using secure token management.

---

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.8+
- Zerodha trading account and API credentials
- API keys for NewsAPI and optionally Twitter API for sentiment analysis

### 2. Installation & Setup

git clone https://github.com/yourusername/stock_ai_trader.git
cd stock_ai_trader
pip install -r requirements.txt
python -m textblob.download_corpora



### 3. Configure API Keys

Edit `config.py` to add your API keys and secrets securely:

ZERODHA_API_KEY = "your_zerodha_api_key"
ZERODHA_API_SECRET = "your_zerodha_api_secret"
NEWS_API_KEY = "your_newsapi_key"
TWITTER_BEARER_TOKEN = "your_twitter_bearer_token"



### 4. Launch the App

streamlit run app.py



### 5. Authenticate & Use

- Open the Zerodha login URL from the sidebar.
- Sign in and copy the `request_token` from the redirected URL.
- Paste the token into the app sidebar to authenticate.
- Select your stocks and specify trading capital.
- Monitor live prices, AI-generated buy/sell signals, portfolio allocation.
- Auto-trade is enabled based on AI signals and risk management controls.

---

## 📊 How It Works

- **Data Collection:** Real-time prices from Zerodha WebSocket; historical data from Yahoo Finance; news from NewsAPI.
- **Feature Engineering:** Smooth traditional technical indicators are calculated on price data for input features.
- **Model Prediction:** Ensemble of AI models predicts next-day stock movement; LSTM and Prophet models enable deep time-series insights.
- **Sentiment Fusion:** Market mood assessed from the latest news articles enhances signal confidence.
- **Risk Controls:** Automatic checks like cooldown periods, position-sizing limits, stop-loss and take-profit ensure safe trading.
- **Order Execution:** Buy/sell signals trigger Zerodha market orders in real-time to implement strategies.
- **User Interface:** Streamlit app provides charts, tables, and controls with live updates and exportable reports.

---

## 🛠️ Project Structure

stock_ai_trader/
│── app.py # Main interactive Streamlit app
│── broker_api.py # Zerodha API integration & live data WebSocket
│── config.py # Config & API keys
│── data_fetcher.py # Stock & news data fetching utilities
│── feature_engineering.py# Technical indicator extraction
│── models.py # Classic ML models (RF, XGBoost)
│── models_lstm.py # LSTM deep learning model
│── models_prophet.py # Prophet forecasting model
│── sentiment.py # News sentiment analysis
│── backtest.py # Historical backtesting module
│── portfolio.py # Portfolio allocation & ranking
│── risk_management.py # Stop-loss, take-profit, cooldown
│── requirements.txt # Python dependencies



---

## 🤝 Contributions & Customization

Feel free to extend the project with:

- Additional ML / DL models or hyperparameter tuning
- Integration of Twitter sentiment or other social media analytics
- Enhanced broker APIs for other platforms or multi-broker support
- Sophisticated UI features and reporting dashboards
- Cloud deployment and scheduling for continuous operation

---

## ⚠️ Safety Notice

- Thoroughly backtest and paper trade before live deployment.
- Trade responsibly with appropriate capital.
- Keep API credentials secure and never share publicly.
- Understand brokerage fees and regulations of live trading.

---

## 📧 Support & Contact

For questions or help, please open issues on GitHub or contact Bhanu@karanwalcapital.com

---

Embark on your journey to smart, automated stock trading powered by AI and real-time data with **Stock AI Trader**!

---

*Ready to trade smarter? Run the app and watch your portfolio evolve.*
