import re
import csv
import string
import random
from typing import Tuple
from nltk import classify, NaiveBayesClassifier
from nltk.corpus import twitter_samples, stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer

# NOTE: following a guide from
# https://www.digitalocean.com/community/tutorials/how-to-perform-sentiment-analysis-in-python-3-using-the-natural-language-toolkit-nltk

clean_pattern = re.compile('[^a-zA-Z0-9_@#\s]+')

def reformat_tokens(tokens: list) -> list:
    return dict([token, True] for token in tokens)

def remove_noise(tokens: list, stop_words: Tuple=()):
    cleaned_tokens = []
    for token in tokens:
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', token)
        token = re.sub("(@[A-Za-z0-9_]+)", "", token)

        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token)

        if len(token) > 0 and token not in string.punctuation and \
           token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())
    return cleaned_tokens

def clean(s: str) -> list:
    return clean_pattern.sub('', s).split()

# read in and tokenize - dataset from
# https://github.com/MohamedAfham/Twitter-Sentiment-Analysis-Supervised-Learning/tree/master/Data
positive_data = []
negative_data = []
with open('train_tweets.csv', 'r', encoding='utf-8') as f:
    for i, line in enumerate(csv.reader(f)):
        if i == 0:
            continue
        if int(line[1]) == 1:
            negative_data.append(
                [clean(line[2]), line[2], int(line[1])]
            )
        else:
            positive_data.append(
                [clean(line[2]), line[2], int(line[1])]
            )
# additionally add in nltk's corpus as well
nltk_pos_tweets = twitter_samples.strings('positive_tweets.json')
nltk_neg_tweets = twitter_samples.strings('negative_tweets.json')
for tweet in nltk_pos_tweets:
    positive_data.append(
        [clean(tweet), tweet, 0]
    )
for tweet in nltk_neg_tweets:
    negative_data.append(
        [clean(tweet), tweet, 1]
    )

stop_words = stopwords.words('english')

# remove links, etc, lemmatize
pos_cleaned_tokens = [remove_noise(d[0], stop_words) for d in positive_data]
neg_cleaned_tokens = [remove_noise(d[0], stop_words) for d in negative_data]

# reformat tokens into a list of dicts like [{'father': True, 'dysfunctional': True, ...}]
pos_model_data = [reformat_tokens(tokens) for tokens in pos_cleaned_tokens]
neg_model_data = [reformat_tokens(tokens) for tokens in neg_cleaned_tokens]

# label lists of tokens either Positive or Negative
pos_dataset = [(d, "Positive") for d in pos_model_data]
neg_dataset = [(d, "Negative") for d in neg_model_data]

# combine and shuffle datasets
dataset = pos_dataset + neg_dataset
random.shuffle(dataset)

# split dataset into train/test 
midpoint = len(dataset) // 2
train_data = dataset[:midpoint]
test_data = dataset[midpoint:]

# train the classifier
classifier = NaiveBayesClassifier.train(train_data)

# analytics
print("Accuracy is:", classify.accuracy(classifier, test_data))
print(classifier.show_most_informative_features(10))

# classification test
custom_tweet = "I ordered just once from TerribleCo, they screwed up, never used the app again."
prepd = reformat_tokens(remove_noise(clean(custom_tweet)))
print(custom_tweet, '->', classifier.classify(prepd))

custom_tweet2 = "I ordered once from SuperCo, they were awesome."
prepd2 = reformat_tokens(remove_noise(clean(custom_tweet2)))
print(custom_tweet2, '->', classifier.classify(prepd2))
import pdb; pdb.set_trace()
