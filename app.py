from flask import Flask, render_template, jsonify
from random import *
from flask_cors import CORS
import requests

app = Flask(__name__,
            static_folder = "./dist",
            template_folder = "./dist")
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    # return requests.get('http://localhost:8080/{}'.format(path)).text
    return render_template("index.html")
