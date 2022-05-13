from database.database import Database


class Purchases(Database):
    def __init__(self, connection):
        super().__init__(connection)
        self.table_name = 'Purchases'
        self.primary_key = 'transaction_id'
