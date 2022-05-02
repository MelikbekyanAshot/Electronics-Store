from database.database import Database


class Shipment(Database):
    def __init__(self, connection):
        super().__init__(connection)
        self.table_name = 'Shipment'
        self.primary_key = 'product_id'
        self.columns = ['category', 'name', 'price', 'amount', 'delivery_time','provider_id', 'storage']
