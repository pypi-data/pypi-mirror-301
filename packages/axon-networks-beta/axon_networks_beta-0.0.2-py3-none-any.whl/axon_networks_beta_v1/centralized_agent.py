class CentralizedAgent:
    def __init__(self, ai_model, max_nodes=10):
        self.nodes = []
        self.ai_model = ai_model
        self.max_nodes = max_nodes

    def register_node(self, node):
        if len(self.nodes) < self.max_nodes:
            self.nodes.append(node)
            print(f"Node '{node.node_id}' registered successfully.")
        else:
            print("Node limit reached, cannot register more nodes.")

    def get_data_from_nodes(self):
        data = {node.node_id: node.fetch_data() for node in self.nodes}
        return data

    def process_data(self, data):
        instructions = self.ai_model.generate_instructions(data)
        return instructions

    def distribute_instructions(self, instructions):
        for node in self.nodes:
            if node.node_id in instructions:
                node.send_command(instructions[node.node_id])

    def run_real_time_process(self):
        data_from_nodes = self.get_data_from_nodes()
        instructions = self.process_data(data_from_nodes)
        self.distribute_instructions(instructions)
