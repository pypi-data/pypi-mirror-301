class SupplyChainNode:
    def __init__(self, node_id, db_connector):
        self.node_id = node_id
        self.db_connector = db_connector

    def fetch_data(self):
        data = self.db_connector.get_inventory_data()
        return data

    def send_command(self, command):
        print(f"Node {self.node_id}: Executed command '{command}'")
        self.db_connector.execute_command(command)
