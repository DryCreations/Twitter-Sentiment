import logging
import pickle
from numpy import argmax
from typing import Tuple
from keras.models import model_from_json
from keras.preprocessing.sequence import pad_sequences


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


    def get_sentiment(self, tweets: list) -> list:
        batch_size = 64
        if len(tweets) < batch_size: batch_size = len(tweets)

        tokenized_tweets = self.tokenizer.texts_to_sequences(tweets)
        tokenized_tweets = pad_sequences(tokenized_tweets, maxlen=39, dtype='int32', value=0)
        results = self.model.predict(tokenized_tweets, batch_size=batch_size, verbose=2)
        sentiments = ['positive' if argmax(s) == 1 else 'negative' for s in results]
        scores = [s[argmax(s)] for s in results]
        return list(zip(tweets, sentiments, scores))
