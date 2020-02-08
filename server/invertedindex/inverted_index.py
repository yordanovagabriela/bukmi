"""
    Inverted Index class.
"""
class InvertedIndex:
    def __init__(self, db):
        self.index = dict()
        self.db = db

    def __repr__(self):
        return str(self.index)
        
    """
        Saves the document to the DB and update the index.
    """
    def add_index(self, keyword, bookmark_id):
        if keyword not in self.index:
            self.index[keyword] = [bookmark_id]
        else:
            occurances = self.index[keyword]
            occurances.append(bookmark_id)
            self.index[keyword] = occurances
    
    """
        Returns the dictionary of terms with their correspondent Appearances. 
        This is a very naive search since it will just split the terms and show
        the documents where they appear.
    """
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