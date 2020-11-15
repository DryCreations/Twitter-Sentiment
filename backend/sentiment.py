import json
import pickle
import logging
from numpy import argmax
from typing import Tuple
from keras.models import model_from_json
from keras.preprocessing.sequence import pad_sequences
from nltk.corpus import stopwords
import re

from nltk.tokenize import word_tokenize


# from backend.sentiment_lstm_keras import clean

stop_words = set(stopwords.words('english'))
def clean(tweets: list) -> list:
    def _clean(s: str) -> str:
        s = re.sub(r"(?:\@|\#|\$|http?\://|https?\://|www)\S+", "", s)
        s = ' '.join(s.split())
        s = re.sub(r'\s+', ' ', s, flags=re.I)
        s = re.sub('[^a-zA-z0-9\s]', '', s)
        tokens = word_tokenize(s)
        filtered = [w for w in tokens if not w in stop_words]
        s = ' '.join(filtered)
        s = re.sub('(\\b[A-Za-z] \\b|\\b [A-Za-z]\\b)', '', s)
        return s
    for tweet in tweets:
        tweet['cleaned'] = _clean(tweet['full_text'])

# stop_words = set(stopwords.words('english'))
class Sentiment:

    def __init__(self):
        self.load_model()
        self.load_tokenizer()


    def load_model(self) -> None:
        with open('backend/model.json', 'r') as f:
            self.model = model_from_json(f.read())
        self.model.load_weights('backend/model.h5')


    def load_tokenizer(self) -> None:
        with open('backend/tokenizer.pickle', 'rb') as handle:
            self.tokenizer = pickle.load(handle)


    def get_sentiment(self, tweets: list):
        batch_size = 64
        if len(tweets) < batch_size: batch_size = len(tweets)

        clean(tweets)

        tweets = [t for t in tweets if len(t['cleaned']) > 0]
        cleaned = [t['cleaned'] for t in tweets]

        tokenized_tweets = self.tokenizer.texts_to_sequences(cleaned)
        tokenized_tweets = pad_sequences(tokenized_tweets, maxlen=39, dtype='int32', value=0)
        results = self.model.predict(tokenized_tweets, batch_size=batch_size, verbose=2)
        sentiment = ['positive' if argmax(s) == 1 else 'negative' for s in results]
        confidence = [s[argmax(s)] for s in results]
        for i in range(len(tweets)):
            tweets[i]['sentiment'] = sentiment[i]
            tweets[i]['confidence'] = json.dumps(str(confidence[i]))
        return tweets
