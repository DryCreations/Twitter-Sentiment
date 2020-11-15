import re
import csv
from typing import Tuple
from textblob import TextBlob
from nltk.corpus import twitter_samples

# NOTE: following guide found here
# https://www.geeksforgeeks.org/twitter-sentiment-analysis-using-python/
# and here
# https://www.analyticsvidhya.com/blog/2018/02/natural-language-processing-for-beginners-using-textblob/

def clean_tweet(tweet: str) -> str:
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", 
        " ", tweet).split()) 

def get_sentiment(tweet: str) -> Tuple:
    try:
        analysis = TextBlob(clean_tweet(tweet))
        if analysis.sentiment.polarity > 0:
            return 'positive', analysis.sentiment.polarity
        elif analysis.sentiment.polarity == 0:
            return 'neutral', analysis.sentiment.polarity
        else:
            return 'negative', analysis.sentiment.polarity
    except:
        print(tweet)
        return 'neutral', 0

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

correct_pos = 0
correct_neg = 0
false_pos = 0
false_neg = 0
neutral = 0
for tweet in positive_data:
    pred_lbl, polarity = get_sentiment(tweet)
    if pred_lbl == 'positive':
        correct_pos += 1
    elif pred_lbl == 'negative':
        false_neg += 1
    else:
        neutral += 1
for tweet in negative_data:
    pred_lbl, polarity = get_sentiment(tweet)
    if pred_lbl == 'negative':
        correct_neg += 1
    elif pred_lbl == 'positive':
        false_pos += 1
    else:
        neutral += 1
print(f'correct_pos: {correct_pos}')
print(f'correct_neg: {correct_neg}')
print(f'false_pos: {false_pos}')
print(f'false_neg: {false_neg}')
print(f'neutral: {neutral}')
total = correct_pos + correct_neg + false_pos + false_neg  # + neutral
print(f'accuracy: {(correct_pos + correct_neg) / total}')

import pdb; pdb.set_trace()
