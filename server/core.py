import requests
import json

from flask import Flask
from flask import request

from html_parser import parse
from keyword_extractor import KeywordExtractor

from nltk.corpus import wordnet 

from invertedindex.inverted_index import InvertedIndex
from invertedindex.database import Database

app = Flask(__name__)

extractor = KeywordExtractor()
database = Database()
inverted_index = InvertedIndex(database)

@app.route('/add', methods=['POST'])
def add():
    url_param = request.get_json()['url']
    content = requests.get(url_param).content
    parsed_content = parse(content)

    keywords = extractor.extract(parsed_content['text'], incl_scores=False)
    
    if database.exists(url_param):
      return "Bookmark {} already exists".format(url_param)

    bookmark = {'url': url_param, 'title': parsed_content['title']}
    bookmark_id = database.add(bookmark)

    debug_keywords = []
    for keyword in keywords:
      inverted_index.add_index(keyword, bookmark_id)
      debug_keywords.append(keyword)

    if app.debug:
      print("Keywords for {}: {}".format(url_param, debug_keywords))

    return "Added successfully bookmark with link {}".format(url_param)

@app.route('/search', methods=['GET'])
def search():
  tags = request.get_json()['tags']

  all_tags = set(tags)
  for tag in tags:
    all_tags = all_tags | retrieve_synonyms(tag)
    
  result = inverted_index.lookup_query(tags)

  return json.dumps(result)

def retrieve_synonyms(word):
  synonyms = []

  for synonym in wordnet.synsets(word): 
    for lemma in synonym.lemmas():
        print(lemma.name())
        synonyms.append(lemma.name()) 

  return set(synonyms)

if __name__ == '__main__':
    app.run(debug=True)