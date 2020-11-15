import re
import csv
import pickle
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from nltk.corpus import twitter_samples, stopwords

# NOTE: following the guide found here
# https://stackabuse.com/python-for-nlp-sentiment-analysis-with-scikit-learn/


def clean(tweet: str) -> str:
    # Remove all the special characters
    processed_feature = re.sub(r'\W', ' ', str(tweet))

    # remove all single characters
    processed_feature= re.sub(r'\s+[a-zA-Z]\s+', ' ', processed_feature)

    # Remove single characters from the start
    processed_feature = re.sub(r'\^[a-zA-Z]\s+', ' ', processed_feature) 

    # Substituting multiple spaces with single space
    processed_feature = re.sub(r'\s+', ' ', processed_feature, flags=re.I)

    # Removing prefixed 'b'
    processed_feature = re.sub(r'^b\s+', '', processed_feature)

    # Converting to Lowercase and remove leading/trailing whitespace
    return processed_feature.lower().strip()

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
nltk_pos_tweets = twitter_samples.strings('positive_tweets.json')
nltk_neg_tweets = twitter_samples.strings('negative_tweets.json')
positive_data += [tweet for tweet in nltk_pos_tweets]
negative_data += [tweet for tweet in nltk_neg_tweets]

print('cleaning...')
positive_cleaned = [clean(d) for d in positive_data]
negative_cleaned = [clean(d) for d in negative_data]

features = positive_cleaned + negative_cleaned
labels = ([1] * len(positive_cleaned)) + ([0] * len(negative_cleaned))

print('vectorizing...')
vectorizer = TfidfVectorizer (max_features=2500, min_df=7, max_df=0.8, stop_words=stopwords.words('english'))
feature_vectors = vectorizer.fit_transform(features).toarray()

X_train, X_test, y_train, y_test = train_test_split(
    feature_vectors, labels, test_size=0.2, random_state=0
)

print('fitting...')
text_classifier = RandomForestClassifier(n_estimators=100, random_state=0)
text_classifier.fit(X_train, y_train)

print('predicting...')
predictions = text_classifier.predict(X_test)

print(confusion_matrix(y_test,predictions))
print(classification_report(y_test,predictions))
print(accuracy_score(y_test, predictions))

pickle.dump(text_classifier, open('saved_model_sklearn', 'wb'))

import pdb; pdb.set_trace()
