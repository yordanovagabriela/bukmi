from storage.persistence_service import PersistenceService
from elasticsearch import Elasticsearch

ENDPOINT_URL = 'https://c7d944ec53ba43069b2313a242cc5ca8.europe-west3.gcp.cloud.es.io:9243'

class ElasticsearchService(PersistenceService):
    def __init__(self):
        self.endpoint_url = ENDPOINT_URL
        self.username = 'elastic'
        self.password = 'oDN2zseIAJBYKWd0fDbfeBva'
        self.index = 'bookmark'
        self._connect()

    def _connect(self):
        client = None
        client = Elasticsearch([self.endpoint_url], http_auth=(self.username, self.password))
        if client.ping():
            print('Connected to Elasticsearch on {}'.format(self.endpoint_url))
        else:
            raise Exception("Cannot connect to Elasticsearch on {}".format(self.endpoint_url))
        self._client = client

    def search(self, query):
        query_result = self._client.search(index=self.index, body=query)
        docs = list(map(lambda hit: hit["_source"], query_result['hits']['hits']))
        return docs

    def index_doc(self, doc):
        # TODO search if exists
        return self._client.index(index=self.index, body=doc)

    def list(self):
        query = {
            "query": {
                "match_all": {}
            }
        }
        return self.search(query)
