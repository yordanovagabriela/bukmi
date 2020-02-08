class InvertedIndex:
    def __init__(self, db):
        self.index = dict()
        self.db = db

    def __repr__(self):
        return str(self.index)
        
    def add_index(self, keyword, bookmark_id):
        if keyword not in self.index:
            self.index[keyword] = [bookmark_id]
        else:
            occurances = self.index[keyword]
            occurances.append(bookmark_id)
            self.index[keyword] = occurances
    
    def lookup_query(self, terms):
        result = []

        for term in terms:
            if term not in self.index:
                continue

            for bookmark_id in self.index[term]:
                bookmark = self.db.get(bookmark_id)
                if bookmark in result:
                    continue

                result.append(self.db.get(bookmark_id))

        return list(result)