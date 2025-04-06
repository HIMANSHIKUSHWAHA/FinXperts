import requests
from datetime import datetime, timedelta
from transformers import pipeline
from agent_communication_bus import AgentCommunicationBus

# 🔑 Finnhub API Key
FINNHUB_API_KEY = "cvorhi1r01qihjtqhsh0cvorhi1r01qihjtqhshg"  

# 🧠 Load HuggingFace sentiment pipeline
sentiment_model = pipeline("sentiment-analysis")

# ----------------------------------------
# 🔍 Fetch stock-related news from Finnhub
# ----------------------------------------
def fetch_stock_news(symbol):
    today = datetime.today().date()
    week_ago = today - timedelta(days=7)

    url = (
        f"https://finnhub.io/api/v1/company-news"
        f"?symbol={symbol}&from={week_ago}&to={today}&token={FINNHUB_API_KEY}"
    )

    try:
        response = requests.get(url)
        response.raise_for_status()
        news_data = response.json()

        if not news_data:
            return {"error": f"No news articles found for {symbol}."}
        return news_data

    except requests.exceptions.RequestException as e:
        return {"error": f"❌ Network error while fetching news for {symbol}: {str(e)}"}
    except Exception as e:
        return {"error": f"❌ Unexpected error: {str(e)}"}

# ----------------------------------------
# 📰 Format news articles + AI sentiment
# ----------------------------------------
def format_news(news_articles):
    formatted_news = []

    for article in news_articles[:5]:  # Limit to top 5
        headline = article.get("headline", "No Title")
        summary = article.get("summary", "No Summary Available")
        url = article.get("url", "#")
        source = article.get("source", "Unknown")
        datetime_field = article.get("datetime", 0)

        try:
            datetime_str = datetime.fromtimestamp(datetime_field).strftime("%Y-%m-%d %H:%M")
        except (ValueError, TypeError):
            datetime_str = "Unknown Date"

        # 🧠 AI Sentiment Analysis
        sentiment_result = sentiment_model(summary[:512])[0]  # truncate long text
        sentiment = f"{sentiment_result['label']} ({sentiment_result['score']:.2f})"

        formatted_news.append({
            "headline": headline,
            "summary": summary,
            "url": url,
            "source": source,
            "datetime_str": datetime_str,
            "sentiment": sentiment
        })

    return formatted_news
