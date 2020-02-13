from storage.elasticsearch_service import ElasticsearchService
from storage.invertedindex_service import InvertedIndex

class PersistenceServiceFactory:
    def getInstance(self, type):
        if type == 'INMEMORY':
            return InvertedIndex()
        elif type == 'ELASTIC':
            return ElasticsearchService()
        else:
            raise ValueError("PersistenceService {} does not exists.".format(type))