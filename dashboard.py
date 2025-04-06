import streamlit as st
import plotly.graph_objs as go
from agent_communication_bus import AgentCommunicationBus
from agent_trading_strategy import TradingStrategyAgent
from agent_execution import ExecutionAgent
from agent_risk_management import RiskManagementAgent
from market_data import fetch_market_data
from news_api import fetch_stock_news, format_news

# --- Page Config ---
st.set_page_config(page_title="FinXperts", layout="wide")

# --- Project Title ---
st.markdown("""
    <h1 style='text-align: center; color: #4CAF50; font-size: 2.5rem;'>
        💼 FinXperts: Financial Multi-Agent Trading System
    </h1>
    <hr style="border: 1px solid #444;">
""", unsafe_allow_html=True)

# --- Initialize Bus + Agents ---
bus = AgentCommunicationBus()
strategy_agent = TradingStrategyAgent(bus)
execution_agent = ExecutionAgent(bus)
risk_agent = RiskManagementAgent(bus)

# --- Session state for button click ---
if "analyze" not in st.session_state:
    st.session_state["analyze"] = False

# --- Sidebar Controls ---
with st.sidebar:
    st.markdown("## 🧊 Controls")
    
    stock_options = [
        'AAPL', 'GOOGL', 'AMZN', 'TSLA', 'MSFT', 'META', 'NVDA', 'NFLX', 'BA', 'SPY',
        'BABA', 'INTC', 'ORCL', 'V', 'JPM', 'DIS', 'PYPL', 'AMD', 'UBER', 'SHOP'
    ]
    selected_stocks = st.multiselect("Select stocks to analyze:", stock_options, default=["AAPL"])
    period = st.slider("Time period (days)", 1, 365, 30)

    # Risk profile with labels
    st.markdown("### Risk Profile")
    risk_profile = st.slider(
        "Select your risk tolerance:",
        0, 100, 60, step=10,
        format="%d",
        help="Conservative to Aggressive"
    )
    risk_label = "Conservative" if risk_profile < 40 else "Balanced" if risk_profile < 70 else "Aggressive"
    st.markdown(f"**Selected:** {risk_label}")

    # Chart type toggle
    chart_type = st.radio("Chart Type", ["📈 Line Chart", "🕯️ Candlestick"], horizontal=True)

    if st.button("📊 Analyze Stocks"):
        st.session_state["analyze"] = True

# --- Tabs ---
tabs = st.tabs(["📈 Dashboard", "🤖 Agent Status", "🔌 Communications", "📂 Data Explorer"])

# -------------------- DASHBOARD ---------------------
with tabs[0]:
    st.markdown("## 📈 Market Analysis Dashboard")

    # Initialize logs
    strategy_logs = []
    execution_logs = []
    risk_logs = []

    if not st.session_state["analyze"] or not selected_stocks:
        st.info("No recommendations available yet. Please select stocks and click 'Analyze Stocks'.")
    else:
        for symbol in selected_stocks:
            st.markdown(f"### 📊 Analysis for {symbol}")
            left_col, right_col = st.columns([3, 1])

            # Fetch real market data
            market_data = fetch_market_data(symbol)

            # Send to agents
            bus.send_message("Dashboard", "TradingStrategyAgent", "market_data", {
                "symbol": symbol,
                "data": market_data.reset_index().to_dict(orient="list")
            })
            bus.send_message("Dashboard", "RiskManagementAgent", "assess_portfolio", {
                "portfolio_value": 2000
            })

            # Run agents
            risk_logs += risk_agent.assess_risk()
            strategy_logs += strategy_agent.generate_signal()
            execution_logs += execution_agent.execute_trade()

            with left_col:
                st.markdown("#### 💡 AI Strategy Output")
                for log in strategy_logs:
                    st.success(log)

                st.markdown("#### 📉 Price Chart")
                if chart_type == "📈 Line Chart":
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=market_data.index, y=market_data['Close'], mode='lines', name='Close Price', line=dict(color='orange')))
                    fig.add_trace(go.Scatter(x=market_data.index, y=market_data['MA50'], mode='lines', name='50-Day MA', line=dict(color='green')))
                    fig.add_trace(go.Scatter(x=market_data.index, y=market_data['MA200'], mode='lines', name='200-Day MA', line=dict(color='red')))
                    fig.update_layout(template="plotly_dark", xaxis_title="Date", yaxis_title="Price", hovermode="x unified")
                    st.plotly_chart(fig, use_container_width=True)

                elif chart_type == "🕯️ Candlestick":
                    fig = go.Figure(data=[
                        go.Candlestick(
                            x=market_data.index,
                            open=market_data['Open'],
                            high=market_data['High'],
                            low=market_data['Low'],
                            close=market_data['Close'],
                            name='Candlestick'
                        )
                    ])
                    fig.update_layout(
                        template="plotly_dark",
                        xaxis_title="Date",
                        yaxis_title="Price",
                        hovermode="x unified"
                    )
                    st.plotly_chart(fig, use_container_width=True)

                if execution_logs:
                    st.subheader("🚀 Trade Executions")
                    for log in execution_logs:
                        st.success(log)

                if risk_logs:
                    st.subheader("🛡️ Risk Assessment")
                    for log in risk_logs:
                        st.warning(log)

            with right_col:
                st.subheader("📰 Latest News")
                news_data = fetch_stock_news(symbol)
                if "error" in news_data:
                    st.error(news_data["error"])
                else:
                    for article in format_news(news_data)[:5]:
                        st.markdown(
                            f"""
                            <div style="
                                border-radius: 6px;
                                background-color: #1f2937;
                                padding: 12px;
                                margin-bottom: 10px;
                                box-shadow: 0 2px 8px rgba(0,0,0,0.15);
                                font-size: 0.85rem;
                            ">
                                <div style="color: #60a5fa; font-weight: bold;">{article['headline']}</div>
                                <div style="color: #d1d5db; font-size: 0.8rem;">{article['summary']}</div>
                                <div style="color: #9ca3af; font-size: 0.75rem;">🕒 {article['datetime_str']} | 📰 {article['source']}</div>
                                <div style="color: #16e0bd; font-size: 0.75rem;">🧠 Sentiment: {article['sentiment']}</div>
                                <a href="{article['url']}" target="_blank" style="color: #facc15;">Read More →</a>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

# -------------------- AGENT STATUS ---------------------
with tabs[1]:
    st.markdown("## 🤖 Agent Status")
    st.markdown("### 🧠 TradingStrategyAgent")
    st.info(strategy_agent.status)

    st.markdown("### 🛡️ RiskManagementAgent")
    st.info(risk_agent.status)

    st.markdown("### 💼 ExecutionAgent")
    st.info(execution_agent.status)

# -------------------- COMMUNICATION ---------------------
with tabs[2]:
    st.markdown("## 🔌 Inter-Agent Communication")
    st.markdown("### 📡 Message Queue")
    if bus.messages:
        for msg in bus.messages:
            st.json(msg)
    else:
        st.info("No messages in the queue. Agents processed and cleared them.")

# -------------------- DATA EXPLORER ---------------------
with tabs[3]:
    st.markdown("## 📂 Data Explorer")
    if st.session_state["analyze"] and selected_stocks:
        st.dataframe(market_data.tail())
    else:
        st.info("Click 'Analyze Stocks' to load data.")
