import time
import string
import re

import numpy as np
import spacy

from collections import OrderedDict
from spacy.lang.en.stop_words import STOP_WORDS

import preprocessor.text_preprocessor as preprocessor

nlp = spacy.load('en_core_web_sm')

class TextRankKeywordExtractor():
    def __init__(self):
        self.damping_coefficient = 0.85
        self.min_difference = 1e-5
        self.steps = 10
        self.node_weight = None
    
    def set_stopwords(self, stopwords):  
        for word in STOP_WORDS.union(set(stopwords)):
            lexeme = nlp.vocab[word]
            lexeme.is_stop = True

    def extract_sentences(self, document, candidate_pos):
        sentences = []

        for sentence in document.sents:
            prsentence = preprocessor.preprocess_sentence(sentence)
            selected_words = []
            for token in prsentence:
                if token.pos_ in candidate_pos and token.is_stop is False:
                    selected_words.append(token.lemma_.lower())
            sentences.append(selected_words)

        return sentences
        
    def build_vocabulary(self, sentences):
        vocabulary = OrderedDict()
        i = 0

        for sentence in sentences:
            for word in sentence:
                if word not in vocabulary:
                    vocabulary[word] = i
                    i += 1
        return vocabulary
    
    def create_token_pairs_by_windows_size(self, window_size, sentences):
        token_pairs = list()

        for sentence in sentences:
            for i, word in enumerate(sentence):
                for j in range(i + 1, i + window_size):
                    if j >= len(sentence):
                        break
                    pair = (word, sentence[j])
                    if pair not in token_pairs:
                        token_pairs.append(pair)
        return token_pairs
        
    def symmetrize(self, matrix):
        return matrix + matrix.T - np.diag(matrix.diagonal())
    
    def create_matrix(self, vocabulary, token_pairs):
        vocabulary_size = len(vocabulary)
        matrix = np.zeros((vocabulary_size, vocabulary_size), dtype='float')

        for word1, word2 in token_pairs:
            i, j = vocabulary[word1], vocabulary[word2]
            matrix[i][j] = 1
            
        matrix = self.symmetrize(matrix)
        
        norm = np.sum(matrix, axis=0)
        matrix_normalized = np.divide(matrix, norm, where=norm!=0)
        
        return matrix_normalized

    def get_keywords(self, number=20):
        node_weight = OrderedDict(sorted(self.node_weight.items(), key=lambda t: t[1], reverse=True))

        keywords = []
        for i, (key, value) in enumerate(node_weight.items()):
            keywords.append(key)
            if i > number:
                break

        return keywords
  
    def analyze(self, text, candidate_pos=['NOUN', 'PROPN', 'VERB'], window_size=4, stopwords=list()):
        self.set_stopwords(stopwords)

        text = preprocessor.preprocess_text(text)
        document = nlp(text)

        sentences = self.extract_sentences(document, candidate_pos)
        vocabulary = self.build_vocabulary(sentences)
        token_pairs = self.create_token_pairs_by_windows_size(window_size, sentences)
        
        normalized_matrix = self.create_matrix(vocabulary, token_pairs)
        pagerank_vector = np.array([1] * len(vocabulary))
        
        previous_pagerank = 0
        for epoch in range(self.steps):
            pagerank_vector = (1 - self.damping_coefficient) + self.damping_coefficient * np.dot(normalized_matrix, pagerank_vector)
            if abs(previous_pagerank - sum(pagerank_vector))  < self.min_difference:
                break
            else:
                previous_pagerank = sum(pagerank_vector)

        node_weight = dict()
        for word, index in vocabulary.items():
            node_weight[word] = pagerank_vector[index]
        
        self.node_weight = node_weight