#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS as stopwords 
from sklearn.feature_extraction.text import CountVectorizer 
from sklearn.base import TransformerMixin 
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC

import string
punctuations = string.punctuation

import spacy
#sen = spacy.load('en')
parser = spacy.load('fr')

#Custom transformer using spaCy 
class predictors(TransformerMixin):
    def transform(self, X, **transform_params):
        return [clean_text(text) for text in X]
    def fit(self, X, y=None, **fit_params):
        return self
    def get_params(self, deep=True):
        return {}

# Basic utility function to clean the text 
def clean_text(text):     
    return text.strip().lower()

#Create spacy tokenizer that parses a sentence and generates tokens
#these can also be replaced by word vectors 
def spacy_tokenizer(sentence):
    tokens = parser(sentence)
    tokens = [tok.lemma_.lower().strip() if tok.lemma_ != "-PRON-" else tok.lower_ for tok in tokens]
    tokens = [tok for tok in tokens if (tok not in stopwords and tok not in punctuations)]
    return tokens

def get_pipe():
    #create vectorizer object to generate feature vectors, we will use custom spacy’s tokenizer
    vectorizer = CountVectorizer(tokenizer = spacy_tokenizer, ngram_range=(1,1))
    classifier = LinearSVC()

    # Create the  pipeline to clean, tokenize, vectorize, and classify 
    pipe = Pipeline([("cleaner", predictors()),
                    ('vectorizer', vectorizer),
                    ('classifier', classifier)])
    return pipe

if __name__ == "__main__":
    from sklearn.metrics import accuracy_score 

    # Load sample data
    train = [('pain paris', 'pos'),          
            ('courses vacances intermarché', 'pos'),
            ('presse vacances', 'pos'),
            ('tabac le chacal', 'neg'),
            ("repas saint-denis", 'neg'),
            ]
    train2 = [('restaurant paris', 'pos'),
            ('amazon bd', 'neg'),
            ("amazon bricolage", 'pos'),
            ('leroy merlin bricolage', 'neg'),          
            ('retrait bnp', 'neg')] 
    test =   [('location vacances', 'pos'),     
            ('bricorama bricolage paris', 'neg'),
            ("ventes privées paris", 'neg'),
            ]
    # Create model and measure accuracy
    pipe = get_pipe()
    pipe.fit([x[0] for x in train+train2], [x[1] for x in train+train2]) 
    pred_data = pipe.predict([x[0] for x in test]) 
    for (sample, pred) in zip(test, pred_data):
        print(sample, pred)
    print("--Accuracy:", accuracy_score([x[1] for x in test], pred_data))

    pipe2 = get_pipe()
    pipe2.fit([x[0] for x in train2], [x[1] for x in train2]) 
    pred_data = pipe2.predict([x[0] for x in test]) 
    for (sample, pred) in zip(test, pred_data):
        print(sample, pred)
    print("--Accuracy:", accuracy_score([x[1] for x in test], pred_data))
