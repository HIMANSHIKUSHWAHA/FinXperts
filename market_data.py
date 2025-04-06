import yfinance as yf
import pandas as pd

def fetch_market_data(symbol="AAPL"):
    # Fetch historical data for the stock (past 30 days)
    stock = yf.Ticker(symbol)
    data = stock.history(period="30d")
    
    # Calculate moving averages
    data['MA50'] = data['Close'].rolling(window=50).mean()  # 50-day moving average
    data['MA200'] = data['Close'].rolling(window=200).mean()  # 200-day moving average
    return data
