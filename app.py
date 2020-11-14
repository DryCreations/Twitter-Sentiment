from flask import Flask, render_template, jsonify, request, abort
from random import *
from flask_cors import CORS
import requests

app = Flask(__name__,
            static_folder = "./dist",
            template_folder = "./dist")
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/api/sentiment', methods=['POST'])
def create_task():
    if not request.json or not 'keywords' in request.json:
        abort(400)
    keywords = request.json['keywords']
    # twitter stuff here
    tweets = [
        {'text': 'test', 'sentiment': 1},
        {'text': 'test 2', 'sentiment': 0.5},
        {'text': 'test 3', 'sentiment': .9},
        {'text': 'test 4', 'sentiment': .1},
        {'text': 'test 5', 'sentiment': 1},
        {'text': 'test 6', 'sentiment': 0},
    ]
    return jsonify({'tweets': tweets, 'keywords': keywords}), 201

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    #return requests.get('http://localhost:8080/{}'.format(path)).text
    return render_template("index.html")
