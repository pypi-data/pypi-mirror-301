class MockCausalAIModel:
    def generate_instructions(self, data):
        instructions = {}
        for node_id, node_data in data.items():
            # Example rule: If stock is less than 50, order more stock.
            if node_data["stock"] < 50:
                instructions[node_id] = "Order more stock"
            else:
                instructions[node_id] = "No action needed"
        return instructions
