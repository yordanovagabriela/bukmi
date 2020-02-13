import requests
import json
from flask import Flask
from flask import request

from storage.persistence_service_factory import PersistenceServiceFactory


from preprocessor.html_parser import parse
from core.keyword_extractor import TextRankKeywordExtractor

from inverted_index.inverted_index import InvertedIndex
from inverted_index.database import Database

from preprocessor.text_preprocessor import retrieve_synonyms
from preprocessor.text_preprocessor import lemmatize
from elastic_client.elasticsearch_client import ElasticsearchClient

app = Flask(__name__)

extractor = TextRankKeywordExtractor()

database = Database()
inverted_index = InvertedIndex(database)

@app.route('/add', methods=['POST'])
def add():
    url_param = request.get_json()['url']

    if database.exists(url_param):
      return "Bookmark {} already exists".format(url_param)

    content = requests.get(url_param).content
    parsed_content = parse(content)

    bookmark = {'url': url_param, 'title': parsed_content['title']}
    bookmark_id = database.add(bookmark)

    extractor.analyze(parsed_content['text'])
    keywords = extractor.get_keywords()

    for keyword in keywords:
      print(keyword)
      inverted_index.add_index(keyword, bookmark_id)

    return "Bookmark {} added successfully".format(url_param)

@app.route('/search', methods=['GET'])
def search():
  tags = request.get_json()['tags']
  # tags = map(lambda tag: lemmatize(tag), tags)
  all_tags = set(tags)
  for tag in tags:
    all_tags = all_tags | retrieve_synonyms(tag)

  result = inverted_index.lookup_query(tags)

  return json.dumps(result)

@app.route('/list', methods=['GET'])
def get():
  bookmarks = list(database.db.values())
  return json.dumps(bookmarks)

if __name__ == '__main__':
    service_inmemory = PersistenceServiceFactory().getInstance('INMEMORY')
    service_elastic = PersistenceServiceFactory().getInstance('ELASTIC')

    bookmark = {'url': 'http://test', 'title': 'wikipedia', 'tags': ['test']}

    query2 = {
            "query": {
                "terms" : {
                    "tags" :["test", "test2"]
                }
            }
        } 

    # service_elastic.index_doc(bookmark)
    print(service_elastic.search(query2))
    print(service_elastic.list())

    # service_inmemory.index_doc(bookmark)
    # print(service_inmemory.search(query2))
    # print(service_inmemory.list())
    #app.run(debug=True)