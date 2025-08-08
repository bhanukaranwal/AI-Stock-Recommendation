import yfinance as yf
from newsapi import NewsApiClient
from config import NEWS_API_KEY

newsapi = NewsApiClient(api_key=NEWS_API_KEY)

def get_stock_data(ticker, period="2y"):
    data = yf.download(ticker, period=period, interval="1d", progress=False)
    return data.dropna()

def get_stock_news(ticker, max_articles=5):
    try:
        articles = newsapi.get_everything(q=ticker, language="en", sort_by="publishedAt", page_size=max_articles)
        return [(a["title"], a["description"]) for a in articles["articles"]]
    except Exception as e:
        print(f"[ERROR] News fetch failed: {e}")
        return []
