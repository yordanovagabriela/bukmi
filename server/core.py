import requests
import json

from flask import Flask
from flask import request

from html_parser import parse
from keyword_extractor import TextRankKeywordExtractor

from inmemory_index.inverted_index import InvertedIndex
from inmemory_index.database import Database

from text_preprocessor import retrieve_synonyms
from text_preprocessor import lemmatize
from elasticsearch_client import ElasticsearchClient

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
    app.run(debug=True)