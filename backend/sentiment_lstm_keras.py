import re
import csv
import pickle
import random
import pandas as pd
import tensorflow as tf
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
from numpy import asarray, zeros
from keras.models import Sequential
from keras.layers import LSTM, Flatten, SpatialDropout1D, Dense
from keras.layers.core import Dense
from keras.layers.embeddings import Embedding
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from nltk.corpus import twitter_samples, stopwords
from imdb import get_imdb

# NOTE: following the guide found here
# https://www.kaggle.com/ngyptr/lstm-sentiment-analysis-keras


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
    tweets = map(_clean, tweets)
    return [t for t in tweets if len(t) > 0]


positive_data = []
negative_data = []

# # adding dataset from
# # https://github.com/MohamedAfham/Twitter-Sentiment-Analysis-Supervised-Learning/tree/master/Data
# print('loading first twitter dataset...')
# with open('train_tweets.csv', 'r', encoding='utf-8') as f:
#     for i, line in enumerate(csv.reader(f)):
#         if i == 0:
#             continue
#         if int(line[1]) == 1: negative_data.append(line[2])
#         else: positive_data.append(line[2])

# # adding dataset from
# # https://www.kaggle.com/arkhoshghalb/twitter-sentiment-analysis-hatred-speech?select=train.csv
# print('loading kaggle twitter dataset...')
# with open('train.csv', 'r', encoding='utf-8') as f:
#     for i, line in enumerate(csv.reader(f)):
#         if i == 0:
#             continue
#         if int(line[1]) == 1: negative_data.append(line[2])
#         else: positive_data.append(line[2])

# # adding nltk's corpus
# print('loading nltk\'s twitter dataset...')
# positive_data += twitter_samples.strings('positive_tweets.json')
# negative_data += twitter_samples.strings('negative_tweets.json')

# adding giant dataset from
# https://www.kaggle.com/kazanova/sentiment140
print('loading giant kaggle dataset...')
with open('training.1600000.processed.noemoticon.csv', 'r', encoding='utf-8') as f:
    for i, line in enumerate(csv.reader(f)):
        if int(line[0]) == 0: negative_data.append(line[5])
        elif int(line[0]) == 4: positive_data.append(line[5])


# adding IMDB movie reviews from
# http://ai.stanford.edu/~amaas/data/sentiment/
# http://ai.stanford.edu/~amaas/papers/wvSent_acl2011.bib
# print('loading imdb dataset...')
# positive_data += get_imdb('pos')
# negative_data += get_imdb('neg')

print('cleaning...')
# positive_data = positive_data[:200000]
# negative_data = negative_data[:200000]
positive_data = clean(positive_data)
negative_data = clean(negative_data)

data = positive_data + negative_data
labels = ([1] * len(positive_data)) + ([0] * len(negative_data))

print(f'found {len(positive_data)} positive')
print(f'found {len(negative_data)} negative')
print(f'found {len(data)} total')
print(f'built {len(labels)} labels')

print('shuffling...')
data = list(zip(data, labels))
random.shuffle(data)

data = pd.DataFrame(
    columns=['Tweet', 'Label'],
    data=data
)
print(data.head())

print('tokenizing...')
max_features = 5000
tokenizer = Tokenizer(num_words=max_features, split=' ')
tokenizer.fit_on_texts(data['Tweet'].values)
X = tokenizer.texts_to_sequences(data['Tweet'].values)

print('saving tokenizer...')
with open('tokenizer.pickle', 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

print('padding...')
X = pad_sequences(X)

print('creating model...')
embed_dim = 128
lstm_out = 196

model = Sequential()
model.add(Embedding(max_features, embed_dim, input_length=X.shape[1]))
model.add(SpatialDropout1D(0.4))
model.add(LSTM(lstm_out, dropout=0.2, recurrent_dropout=0.2))
model.add(Dense(2,activation='softmax'))
model.compile(loss = 'categorical_crossentropy', optimizer='adam',metrics = ['accuracy'])
print(model.summary())

print('splitting...')
Y = pd.get_dummies(data['Label']).values
X_train, X_test, Y_train, Y_test = train_test_split(
    X, Y, test_size=0.33, random_state=42
)

print(f'fitting on {len(X_train)} tweets...')
batch_size = 512
epochs = 15
with tf.device("gpu:0"):
    model.fit(
        X_train, Y_train, 
        epochs=epochs, 
        batch_size=batch_size, 
        verbose=2
    )

print('evaluating...')
score, acc = model.evaluate(
    X_test, Y_test,
    verbose=2,
    batch_size=batch_size
)
print("score: %.2f" % (score))
print("acc: %.2f" % (acc))

print('saving to model...')
model_json = model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)
model.save_weights("model.h5")

print('\nDone.')

import pdb; pdb.set_trace()
