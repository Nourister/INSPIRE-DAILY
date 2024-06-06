from pymongo import MongoClient
import app.config as config

client = MongoClient(config.MONGO_URI)
db = client.quotesdb
quotes_collection = db.quotes

quotes = [
    {"text": "The best way to get started is to quit talking and begin doing.", "author": "Walt Disney"},
    {"text": "The pessimist sees difficulty in every opportunity. The optimist sees opportunity in every difficulty.", "author": "Winston Churchill"},
    {"text": "Don’t let yesterday take up too much of today.", "author": "Will Rogers"},
    {"text": "You learn more from failure than from success. Don’t let it stop you. Failure builds character.", "author": "Unknown"},
    {"text": "It’s not whether you get knocked down, it’s whether you get up.", "author": "Vince Lombardi"}
]

quotes_collection.insert_many(quotes)
print("Quotes inserted successfully!")
