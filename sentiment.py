from textblob import TextBlob

def compute_sentiment(news_list):
    sentiments = []
    for title, desc in news_list:
        text = f"{title} {desc if desc else ''}"
        polarity = TextBlob(text).sentiment.polarity
        sentiments.append(polarity)
    if sentiments:
        avg_sentiment = sum(sentiments) / len(sentiments)
    else:
        avg_sentiment = 0
    return avg_sentiment
