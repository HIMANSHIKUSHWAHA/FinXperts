import yfinance as yf
import pandas as pd

def fetch_market_data(symbol="AAPL"):
    """
    Fetch historical stock data for the past 30 days with moving averages.
    
    Args:
        symbol (str, optional): Stock ticker symbol. Defaults to "AAPL".
    
    Returns:
        pandas.DataFrame: Historical stock data with moving averages
    """
    try:
        # Fetch historical data for the stock (past 30 days)
        stock = yf.Ticker(symbol)
        
        # Use a longer period to ensure enough data for moving averages
        data = stock.history(period="3mo")  # Fetch 3 months of data
        
        # Ensure we have enough data for moving averages
        if len(data) < 200:
            print(f"Warning: Insufficient data for {symbol}. Fetched {len(data)} days of data.")
        
        # Calculate moving averages
        data['MA50'] = data['Close'].rolling(window=50, min_periods=1).mean()
        data['MA200'] = data['Close'].rolling(window=200, min_periods=1).mean()
        
        # Return only the last 30 days
        return data.tail(30)
    
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return pd.DataFrame()  # Return an empty DataFrame if there's an error