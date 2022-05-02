from database.database import Database


class Providers(Database):
    def __init__(self, connection):
        super().__init__(connection)
        self.table_name = 'Providers'
        self.primary_key = 'provider_id'
        self.columns = ['name', 'email', 'telephone', 'address']
