from database.database import Database


class Storage(Database):
    def __init__(self, connection):
        super(Storage, self).__init__(connection)
        self.table_name = 'Storage'
        self.primary_key = 'id'
        self.columns = ['category', 'name', 'price', 'amount', 'storage', 'placement', 'provider_id']
