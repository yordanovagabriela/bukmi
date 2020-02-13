import requests
import json
from flask import Flask
from flask import request

from storage.persistence_service_factory import PersistenceServiceFactory

from preprocessor.html_parser import parse
from core.keyword_extractor import TextRankKeywordExtractor

from preprocessor.text_preprocessor import retrieve_synonyms
from preprocessor.text_preprocessor import lemmatize

app = Flask(__name__)

extractor = TextRankKeywordExtractor()
persistence_service = PersistenceServiceFactory().getInstance('ELASTIC')

@app.route('/add', methods=['POST'])
def add():
    url = request.get_json()['url']
    content = requests.get(url).content

    parsed_content = parse(content)
    title = parsed_content['title']
    text = parsed_content['text']

    extractor.analyze(text)
    tags = extractor.get_keywords()

    doc = {'url': url, 'title': title, 'tags': tags}

    persistence_service.index_doc(doc)
    return "Bookmark {} added successfully".format(url)

@app.route('/search', methods=['GET'])
def search():
  tags = request.get_json()['tags']

  all_tags = set(tags)
  for tag in tags:
    all_tags = all_tags | retrieve_synonyms(tag)

  query = {
              "query": {
                  "terms" : {
                      "tags" : tags
                  }
              }
          } 

  result = persistence_service.search(query)

  return json.dumps(result)

@app.route('/list', methods=['GET'])
def get():
  docs = persistence_service.list()
  return docs

if __name__ == '__main__':
    app.run(debug=True)