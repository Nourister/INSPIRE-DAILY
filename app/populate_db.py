from app import db
from app.models import Quote

# List of quotes to add
quotes_data = [
    {"text": "The best way to get started is to quit talking and begin doing.", "author": "Walt Disney"},
    {"text": "The pessimist sees difficulty in every opportunity. The optimist sees opportunity in every difficulty.", "author": "Winston Churchill"},
    {"text": "Don’t let yesterday take up too much of today.", "author": "Will Rogers"},
    {"text": "You learn more from failure than from success. Don’t let it stop you. Failure builds character.", "author": "Unknown"},
    {"text": "It’s not whether you get knocked down, it’s whether you get up.", "author": "Vince Lombardi"}
]

# Function to add quotes to the database
def add_quotes():
    for quote_data in quotes_data:
        quote = Quote(text=quote_data['text'], author=quote_data['author'])
        db.session.add(quote)
    db.session.commit()

# Run this function to add quotes to the database
if __name__ == '__main__':
    add_quotes()
    print("Quotes added successfully!")