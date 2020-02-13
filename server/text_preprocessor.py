from nltk.corpus import wordnet
from nltk.tokenize import TweetTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.tag import pos_tag

import re
import string

def remove_numbers(text):
    return re.sub(r'\d+', '', text)

def remove_punctuation(text):
    return text.translate(str.maketrans('', '', string.punctuation + "”“"))

def preprocess_text(text):
    text = remove_punctuation(text)
    text = remove_numbers(text)
    return text.lower()

def preprocess_sentence(sentence):
    sentence = filter(lambda token: token.text != "”" or token.text != "“", sentence)
    sentence = filter(lambda token: len(token.text) != 1, sentence)
    return sentence

def retrieve_synonyms(word):
  synonyms = []

  for synonym in wordnet.synsets(word): 
    for lemma in synonym.lemmas():
        synonyms.append(lemma.name()) 

  return set(synonyms)

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