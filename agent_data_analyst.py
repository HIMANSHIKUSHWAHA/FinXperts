import yfinance as yf
import pandas as pd
from agent_communication_bus import AgentCommunicationBus

class DataAnalystAgent:
    def __init__(self, bus):
        self.name = "DataAnalystAgent"
        self.bus = bus
        self.status = "Idle"  # Add this line

    def fetch_market_data(self, symbol="AAPL"):
        try:
            self.status = f"📡 Fetching market data for {symbol}..."
            
            # Fetch real market data
            stock = yf.Ticker(symbol)
            data = stock.history(period="30d")

            if data.empty:
                self.status = "❌ No data received."
                return pd.DataFrame()

            # Calculate moving averages
            data['MA50'] = data['Close'].rolling(window=50).mean()
            data['MA200'] = data['Close'].rolling(window=200).mean()

            # Send to StrategyAgent
            self.bus.send_message(
                sender=self.name,
                recipient="TradingStrategyAgent",
                message_type="market_data",
                content={"symbol": symbol, "data": data.reset_index().to_dict(orient="list")}
            )

            self.status = f"✅ Market data for {symbol} processed."
            return data

        except Exception as e:
            self.status = f"❌ Error: {str(e)}"
            return pd.DataFrame()
