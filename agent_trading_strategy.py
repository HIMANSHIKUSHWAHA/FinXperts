import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib
import os
from agent_communication_bus import AgentCommunicationBus

class TradingStrategyAgent:
    def __init__(self, bus):
        self.name = "TradingStrategyAgent"
        self.bus = bus
        self.status = "Idle 💤"

        # 🧠 Load pre-trained ML model if available
        model_path = "models/price_predictor_model.joblib"
        self.use_custom_model = os.path.exists(model_path)
        self.model = joblib.load(model_path) if self.use_custom_model else LinearRegression()

    def generate_signal(self):
        messages = self.bus.get_messages_for(self.name)
        logs = []

        if not messages:
            self.status = "🤔 Waiting for market data..."
            return logs

        for msg in messages:
            if msg["type"] == "market_data":
                content = msg["content"]
                symbol = content["symbol"]
                df = pd.DataFrame(content["data"])

                if 'Close' not in df.columns and 'Price' in df.columns:
                    df['Close'] = df['Price']

                if len(df) < 5:
                    logs.append(f"{symbol}: Not enough data to generate signal.")
                    continue

                features = self.extract_features(df)

                try:
                    if self.use_custom_model:
                        predicted_price = self.model.predict([features])[0]
                    else:
                        # Fallback: use index-based regression
                        X = np.array(range(len(df))).reshape(-1, 1)
                        y = df['Close'].values
                        self.model.fit(X, y)
                        predicted_price = self.model.predict([[len(df)]])[0]
                    
                    current_price = df['Close'].iloc[-1]
                    trend = "Buy" if predicted_price > current_price else "Sell"

                    logs.append(f"{symbol}: Predicted = {predicted_price:.2f}, Signal = {trend}")
                    self.status = f"📈 {symbol} → {trend} (Predicted: {predicted_price:.2f})"

                    self.bus.send_message(
                        sender=self.name,
                        recipient="ExecutionAgent",
                        message_type="trade_signal",
                        content={"symbol": symbol, "signal": trend}
                    )

                except Exception as e:
                    logs.append(f"{symbol}: ❌ Error predicting price: {str(e)}")
                    self.status = "⚠️ Model Error"

        self.bus.clear_messages_for(self.name)
        return logs

    def extract_features(self, df):
        """
        Extract meaningful features for model input.
        Example includes basic statistical indicators.
        """
        close = df['Close']

        features = [
            close.iloc[-1],  # Last price
            close.mean(),    # Mean price
            close.std(),     # Volatility
            close.max(),     # Max price
            close.min(),     # Min price
            close.pct_change().dropna().mean(),  # Average return
            df['Close'].rolling(5).mean().iloc[-1],  # 5-day MA
        ]

        return features
