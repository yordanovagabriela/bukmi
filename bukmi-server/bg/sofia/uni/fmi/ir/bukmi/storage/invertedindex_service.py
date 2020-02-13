import json
from storage.persistence_service import PersistenceService

class InvertedIndex(PersistenceService):
    def __init__(self):
        self.index = dict()
        self.db = Database()

    def search(self, query):
        result = []
        terms = query['query']['terms']['tags']

        for term in terms:
            if term not in self.index:
                continue

            for bookmark_id in self.index[term]:
                bookmark = self.db.get(bookmark_id)
                if bookmark in result:
                    continue

                result.append(self.db.get(bookmark_id))

        return list(result)

    def index_doc(self, doc):
        if self.db.exists(doc['url']):
            return False
    
        tags = doc['tags']

        doc.pop('tags')
        doc_id = self.db.add(doc)

        for tag in tags:
            if tag not in self.index:
                self.index[tag] = [doc_id]
            else:
                occurances = self.index[tag]
                occurances.append(doc_id)
                self.index[tag] = occurances

            return True

    def list(self):
        docs = list(self.db.db.values())
        return json.dumps(docs)

class Database:
    def __init__(self):
        self.db = dict()
        self.id = 0

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
