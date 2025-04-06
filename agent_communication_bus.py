class AgentCommunicationBus:
    def __init__(self):
        self.messages = []

    def send_message(self, sender, recipient, message_type, content):
        self.messages.append({
            "from": sender,
            "to": recipient,
            "type": message_type,
            "content": content
        })

    def get_messages_for(self, recipient):
        return [m for m in self.messages if m['to'] == recipient]

    def clear_messages_for(self, recipient):
        self.messages = [m for m in self.messages if m['to'] != recipient]
