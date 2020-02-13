import logging
from elasticsearch import Elasticsearch

ENDPOINT_URL = 'https://c7d944ec53ba43069b2313a242cc5ca8.europe-west3.gcp.cloud.es.io:9243'

class ElasticsearchClient:
    def __init__(self):
        self.endpoint_url = ENDPOINT_URL
        self.username = 'elastic'
        self.password = 'j2EcY8m3qoRSQbBHCpZlgLox'

    def connect(self):
        _es = None
        _es = Elasticsearch([ENDPOINT_URL], http_auth=(self.username, self.password))
        if _es.ping():
            print('Connected to Elasticsearch on {}'.format(ENDPOINT_URL))
        else:
            raise Exception("Cannot connect to Elasticsearch on {}".format(ENDPOINT_URL))
        self.es = _es

    def index(self, index, doc):
        return self.es.index(index=index, body=doc)

    def search(self, index, query):
        bookmarks = []
        query_result = self.es.search(index=index, body=query)

        for hit in query_result['hits']['hits']:
            bookmarks.append(hit["_source"])
            print(hit["_source"])

        return bookmarks

if __name__ == '__main__':
    elasticsearch = ElasticsearchClient()
    elasticsearch.connect()

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
                        "tags" :["test1", "test3"]
                    }
                }
            } 
    

    # es.indices.delete(index='bookmark')
    #index(es, {"url": "http://www.wikipedia.com", "title": "Wikipedia", "tags": ["test3"]})
    # search(es, query1)
    elasticsearch.search(query2)