from app import app
from flask import Flask, render_template, request, jsonify, url_for
from pymongo import MongoClient
import random 
import config

app = Flask(__name__)
client = MongoClient(config.MONGO_URI)
db = client.quotesdb
quotes_collection = db.quotes

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_quote', methods=['GET'])
def get_quote():
    quotes = list(quotes_collection.find())
    if quotes:
        quote = random.choice(quotes)
        return jsonify({'quote': quote['text'], 'author': quote['author']})



if __name__ == "__main__":
    app.run(debug=True)