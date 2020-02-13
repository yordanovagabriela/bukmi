import logging
from elasticsearch import Elasticsearch

ENDPOINT_URL = 'https://c7d944ec53ba43069b2313a242cc5ca8.europe-west3.gcp.cloud.es.io:9243'

class ElasticsearchClient:
    def __init__(self, config):
        # TODO config class
        self.endpoint_url = ENDPOINT_URL
        self.username = 'elastic'
        self.password = 'oDN2zseIAJBYKWd0fDbfeBva'
        self._connect()

    def _connect(self):
        client = None
        client = Elasticsearch([self.endpoint_url], http_auth=(self.username, self.password))
        if client.ping():
            print('Connected to Elasticsearch on {}'.format(self.endpoint_url))
        else:
            raise Exception("Cannot connect to Elasticsearch on {}".format(self.endpoint_url))
        self._client = client

    def index(self, index, doc):
        return self._client.index(index=index, body=doc)

    def search(self, index, query):
        query_result = self._client.search(index=index, body=query)
        docs = list(map(lambda hit: hit["_source"], query_result['hits']['hits']))
        return docs

if __name__ == '__main__':
    elasticsearch = ElasticsearchClient(None)

    query1 = {
        "query": {
            "match": {
                "url": "http://www.wikipedia.com"
            }
        }
    }

    query2 = {
                "query": {
                    "terms" : {
                        "tags" :["test1", "test2"]
                    }
                }
            } 

    # es.indices.delete(index='bookmark')
    #index(es, {"url": "http://www.wikipedia.com", "title": "Wikipedia", "tags": ["test3"]})
    # search(es, query1)
    elasticsearch.search("bookmark", query2)