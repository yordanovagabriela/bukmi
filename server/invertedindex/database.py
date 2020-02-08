class Database:
    def __init__(self):
        self.db = dict()
        self.id = 0

    def __repr__(self):
        return str(self.__dict__)
    
    def get(self, id):
        return self.db.get(id)

    def exists(self, url):
        for id in self.db:
            if self.db[id]['url'] == url:
                return True
        return False
    
    def add(self, bookmark):
        self.db.update({self.id: bookmark})

        current_id = self.id
        self.id += 1

        return current_id

    def remove(self, id):
        return self.db.pop(id, None)