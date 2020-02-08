import nltk
import re
import string
import operator

from nltk.tokenize import TweetTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.tag import pos_tag

nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')


def toLowercase(content):
  return content.lower()

def remove_numbers(content):
  return re.sub(r'\d+', '', content)

def remove_punctuation(content):
  return content.translate(str.maketrans('', '', string.punctuation + "”“"))

def tokenize(content):
    tokenizer = TweetTokenizer()
    return tokenizer.tokenize(content)

def isPunct(word):
  return len(word) == 1 and word in string.punctuation

def isNumeric(word):
  try:
    float(word) if '.' in word else int(word)
    return True
  except ValueError:
    return False

def lemmatize(word):
    lemmatizer = WordNetLemmatizer()

    result = pos_tag(word)
    if (result is None) or (len(result) == 0):
        return word
    
    tag = result[0][1]

    if tag.startswith("NN"):
        return lemmatizer.lemmatize(word, pos='n')
    elif tag.startswith('VB'):
        return lemmatizer.lemmatize(word, pos='v')
    elif tag.startswith('JJ'):
        return lemmatizer.lemmatize(word, pos='a')
    else:
        return word
 
class KeywordExtractor:

  def __init__(self):
    self.stopwords = set(nltk.corpus.stopwords.words())
    self.top_fraction = 3

  def _generate_candidate_keywords(self, sentences):
    phrase_list = []

    for sentence in sentences:
      words = map(lambda x: "|" if x in self.stopwords else x, nltk.word_tokenize(sentence.lower()))
      words = map(lambda x: x.strip(), words)
      words = map(lambda x: remove_numbers(x), words)
      words = filter(lambda x: x != "”" or x != "“", words)
      words = map(lambda x: remove_punctuation(x) if len(x) > 1 else x , words)
      words = map(lambda x: "|" if x in self.stopwords else x, words)
      words = map(lambda x: "|" if len(x) == 1 and not isPunct(x) else x, words)

      words = map(lambda x: lemmatize(x), words)

      phrase = []
      for word in words:
        if word == "|" or isPunct(word):
          if len(phrase) > 0:
            phrase_list.append(phrase)
            phrase = []
        else:
          phrase.append(word)

    return phrase_list

  def _calculate_word_scores(self, phrase_list):
    word_freq = nltk.FreqDist()
    word_degree = nltk.FreqDist()

    for phrase in phrase_list:
      degree = len(list(filter(lambda x: not isNumeric(x), phrase))) - 1
      for word in phrase:
        word_freq[word] += 1
        word_degree[word] += degree

    for word in word_freq.keys():
      word_degree[word] = word_degree[word] + word_freq[word]

    word_scores = {}
    for word in word_freq.keys():
      word_scores[word] = word_degree[word] / word_freq[word]

    return word_scores
    
  def extract(self, text, incl_scores=False):
    sentences = nltk.sent_tokenize(text)
    phrase_list = self._generate_candidate_keywords(sentences)

    word_scores = self._calculate_word_scores(phrase_list)
    sorted_word_scores = sorted(word_scores.items(), key=operator.itemgetter(1), reverse=True)
    n_words = len(sorted_word_scores)

    if incl_scores:
    #   return sorted_word_scores[0:int(n_words/self.top_fraction)]
        return sorted_word_scores[0:15]
    else:
    #   return map(lambda x: x[0], sorted_word_scores[0:int(n_words/self.top_fraction)])
        return map(lambda x: x[0], sorted_word_scores[0:15])