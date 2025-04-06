## 📘 FinXperts: AI-Powered Multi-Agent Trading System

**FinXperts** is an intelligent, autonomous trading assistant powered by a **multi-agent system (MAS)**. Each agent specializes in a different aspect of trading: strategy, execution, risk management, data analysis, and news interpretation — all collaborating in real-time through a communication bus.

<br>

### 🚀 Features

- 🧠 **Autonomous Agents**  
  Each agent runs independently and makes AI-driven decisions:
  - `TradingStrategyAgent`: Generates buy/sell signals using ML
  - `ExecutionAgent`: Executes trades based on agent signals
  - `RiskManagementAgent`: Monitors portfolio risk and suggests adjustments
  - `DataAnalystAgent`: Processes patterns and anomalies (optional)
  - `News API`: Analyzes news sentiment using HuggingFace Transformers

- 📡 **Agent Communication Bus**  
  A message-passing system that enables agents to interact modularly.

- 📊 **Interactive Dashboard (Streamlit)**  
  Visualize trends, toggle chart styles (line or candlestick), and review AI signals, news, and risk outputs.

- 🤖 **Integrated AI/ML Models**  
  - Linear Regression or custom ML model for price prediction
  - HuggingFace BERT-based sentiment analysis on stock news

---

### 🛠️ Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **Visualization**: [Plotly](https://plotly.com/)
- **Data**: [Yahoo Finance](https://www.yfinance.com/), [Finnhub News](https://finnhub.io/)
- **ML**: `scikit-learn`, `transformers`, `torch`, `joblib`

---

### 🧩 System Architecture

```
User → Streamlit UI → Agents ←→ Market Data, News API
                           ↓
                    Communication Bus
                           ↓
               AI Model Inference (ML, NLP)
```

---

### 📦 Installation

```bash
git clone https://github.com/your-username/FinXperts.git
cd FinXperts
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

---

### ▶️ Run the App

```bash
streamlit run dashboard.py
```

Open your browser to:  
`http://localhost:8501`

---

### 🔑 API Key Setup

Edit `news_api.py` and replace this line with your own [Finnhub API key](https://finnhub.io/):

```python
FINNHUB_API_KEY = "your_finnhub_api_key"
```

---

### 📁 Project Structure

```
FinXperts/
│
├── dashboard.py                # Main Streamlit UI
├── requirements.txt
│
├── agent_communication_bus.py # Message-passing system
├── agent_trading_strategy.py  # Signal generation (ML/Regression)
├── agent_execution.py         # Executes trades
├── agent_risk_management.py   # Risk analysis logic
├── agent_data_analyst.py      # Optional data insights agent
│
├── market_data.py             # Stock data from yfinance
├── news_api.py                # Finnhub + NLP sentiment
└── models/                    # (Optional) Pretrained model files
```

---

### 🧠 Future Enhancements

- [ ] Reinforcement learning for dynamic trading policies  
- [ ] Portfolio allocation optimizers  
- [ ] Multi-threaded agent execution  
- [ ] Real-time stock price monitoring

---

### 👨‍💻 Author

**Himanshi**  
💼 AI Developer | FinTech Enthusiast

