from flask import Flask, render_template, jsonify, request, abort, session, redirect, escape
import random
from flask_cors import CORS
import requests
import tweepy
import os
import json
from dotenv import load_dotenv
from flask_session import Session

from backend.sentiment import Sentiment

load_dotenv()

app = Flask(__name__,
            static_folder = "./dist/static",
            template_folder = "./dist")

cors = CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

app.config['SECRET_KEY'] = os.getenv('SESSION_SECRET')
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

consumer_key = os.getenv('TWITTER_CONSUMER_KEY')
consumer_secret = os.getenv('TWITTER_CONSUMER_SECRET')
callback = os.getenv('TWITTER_CALLBACK')

sentiment = Sentiment()

@app.route('/auth')
def auth():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback)
    url = auth.get_authorization_url()
    session['request_token'] = auth.request_token
    return redirect(url)

@app.route('/callback')
def twitter_callback():
    request_token = session['request_token']
    del session['request_token']

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback)
    auth.request_token = request_token
    verifier = request.args.get('oauth_verifier')
    auth.get_access_token(verifier)
    session['token'] = (auth.access_token, auth.access_token_secret)

    return redirect('/')

@app.route('/api/sentiment', methods=['POST'])
def get_tweets():
    if not request.json or not 'keywords' in request.json or not 'token' in session:
        abort(400)

    token, token_secret = session['token']
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback)
    auth.set_access_token(token, token_secret)
    api = tweepy.API(auth)

    keywords = list(map(lambda s: "\"" + escape(s) + "\"", request.json['keywords']))
    tweets = []
    query = ' '.join(keywords)
    query += ' -filter:retweets'
    for tweet in tweepy.Cursor(api.search, q=query, count=100, tweet_mode="extended", result_type="popular").items(1000):
        tweet_json = tweet._json
        tweets.append(tweet_json)

    tweets = sentiment.get_sentiment(tweets)

    return jsonify({'tweets': tweets, 'keywords': keywords}), 201

@app.route('/api/check_auth', methods=['GET'])
def check_auth():
    return jsonify({'loggedIn': 'token' in session}), 201

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    # return requests.get('http://localhost:8080/{}'.format(path)).text
    return render_template("index.html")
