class MockDBConnector:
    def __init__(self, stock):
        self.stock = stock

    def get_inventory_data(self):
        # Example data
        return {"stock": self.stock}

    def execute_command(self, command):
        print(f"Executing command: {command}")
