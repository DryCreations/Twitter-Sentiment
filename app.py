from flask import Flask, render_template, jsonify, request, abort, session, redirect
from random import *
from flask_cors import CORS
import requests
import tweepy

app = Flask(__name__,
            static_folder = "./dist",
            template_folder = "./dist")

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

consumer_key = TWITTER_CONSUMER_KEY
consumer_secret = TWITTER_CONSUMER_SECRET
app.secret_key = SESSION_SECRET
callback = TWITTER_CALLBACK

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
def create_task():
    if not request.json or not 'keywords' in request.json or not 'token' in session:
        abort(400)

    token, token_secret = session['token']
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback)
    auth.set_access_token(token, token_secret)
    api = tweepy.API(auth)

    keywords = request.json['keywords']
    tweets = []
    for tweet in tweepy.Cursor(api.search, q='test').items(10):
        tweets.append(tweet.text)
    return jsonify({'tweets': tweets, 'keywords': keywords}), 201

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    # return requests.get('http://localhost:8080/{}'.format(path)).text
    return render_template("index.html")
