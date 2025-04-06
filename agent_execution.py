from agent_communication_bus import AgentCommunicationBus
class ExecutionAgent:
    def __init__(self, bus):
        self.name = "ExecutionAgent"
        self.bus = bus
        self.status = "Idle 💤"

    def execute_trade(self):
        messages = self.bus.get_messages_for(self.name)
        result_logs = []

        for msg in messages:
            if msg["type"] == "trade_signal":
                symbol = msg["content"]["symbol"]
                action = msg["content"]["signal"]
                result = f"🚀 Trade executed: {action} {symbol}"
                result_logs.append(result)
                self.status = result

                self.bus.send_message(
                    sender=self.name,
                    recipient="AgentStatusLogger",
                    message_type="trade_executed",
                    content={"symbol": symbol, "action": action, "status": "executed"}
                )

        self.bus.clear_messages_for(self.name)
        if not result_logs:
            self.status = "💼 No trades executed"
        return result_logs
