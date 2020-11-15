import re
import csv
import pickle
import pandas as pd
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

# NOTE: following the guide found here
# https://www.kaggle.com/ngyptr/lstm-sentiment-analysis-keras


def clean(s: str) -> str:
    s = re.sub(r'\s+', ' ', s, flags=re.I)
    s = re.sub('[^a-zA-z0-9\s]', '', s)
    return s.lower().strip()

# read in and tokenize - dataset from
# https://github.com/MohamedAfham/Twitter-Sentiment-Analysis-Supervised-Learning/tree/master/Data
positive_data = []
negative_data = []
with open('train_tweets.csv', 'r', encoding='utf-8') as f:
    for i, line in enumerate(csv.reader(f)):
        if i == 0:
            continue
        if int(line[1]) == 1: negative_data.append(line[2])
        else: positive_data.append(line[2])
# additionally add in nltk's corpus as well
positive_data += twitter_samples.strings('positive_tweets.json')
negative_data += twitter_samples.strings('negative_tweets.json')

labels = ([1] * len(positive_data)) + ([0] * len(negative_data))
data = pd.DataFrame(
    columns=['Tweets', 'Labels'], 
    data=zip(
        positive_data + negative_data, 
        labels
    )
)

print('shuffling')
data.sample(frac=1)

print('cleaning...')
data['Tweets'].apply(clean)

print(data.head())

print('tokenizing...')
max_features = 5000
tokenizer = Tokenizer(num_words=max_features, split=' ')
tokenizer.fit_on_texts(data['Tweets'].values)
X = tokenizer.texts_to_sequences(data['Tweets'].values)

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
Y = pd.get_dummies(data['Labels']).values
X_train, X_test, Y_train, Y_test = train_test_split(
    X, Y, test_size=0.33, random_state=42
)

print('fitting...')
batch_size = 64
epochs = 7
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

print('saving to file...')
model_json = model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)
model.save_weights("model.h5")

print('Done.')

# print(confusion_matrix(y_test, predictions))
# print(classification_report(y_test, predictions))
# print(accuracy_score(y_test, predictions))

import pdb; pdb.set_trace()
