from collections import defaultdict
from src.storage.storage import Storage 


class Index:
    def __init__(self, db_name, name):
        self.storage = Storage(db_name, name)
        self.indexes = defaultdict(dict)

    def get_all_indexes(self):
        pass

    def insert(self, table_name: str, field: str):
        """Создать индекс для поля `field` в таблице `table_name`."""
        data = self.storage.get_from_data_file(table_name)
        self.indexes[(table_name, field)] = defaultdict(list)
        for idx, row in enumerate(data):
            key = row.get(field)
            if key is not None:
                self.indexes[(table_name, field)][key].append(idx) 

    