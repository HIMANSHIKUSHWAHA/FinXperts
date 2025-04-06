class RiskManagementAgent:
    def __init__(self, bus):
        self.name = "RiskManagementAgent"
        self.bus = bus
        self.status = "Idle 💤"  # Default status

    def assess_risk(self):
        messages = self.bus.get_messages_for(self.name)
        logs = []

        if not messages:
            self.status = "🕵️ No portfolio data to assess."
        else:
            for msg in messages:
                if msg["type"] == "assess_portfolio":
                    value = msg["content"]["portfolio_value"]
                    risk_score = value * 0.05

                    if risk_score > 2000:
                        status = "⚠️ High Risk - Immediate action needed"
                    elif risk_score > 1000:
                        status = "⚠️ Medium Risk - Monitor closely"
                    else:
                        status = "✅ Low Risk"

                    logs.append(f"Portfolio: ${value} → {status}")
                    self.status = status  # Update current status dynamically

                    self.bus.send_message(
                        sender=self.name,
                        recipient="TradingStrategyAgent",
                        message_type="risk_evaluation",
                        content={"portfolio_value": value, "risk_status": status}
                    )

        self.bus.clear_messages_for(self.name)
        return logs
