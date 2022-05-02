from database.database import Database


class Purchases(Database):
    def __init__(self, connection):
        super().__init__(connection)
        self.table_name = 'Purchases'
        self.primary_key = 'purchase_id'
        self.columns = ['customer_id', 'product_id', 'amount', 'date', 'sum', 'discount', 'address', 'payment_method']