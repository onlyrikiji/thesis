import csv
import requests
from dotenv import load_dotenv 
import os 
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from flaskblog import create_app, db  # Assuming create_app function is defined in flaskblog/__init__.py
from flaskblog.models import Post
from flask_login import current_user
import time

load_dotenv('.env')
api_url = os.environ.get('API_BASE_URL')

def analyze_sentiment(text):
    # Perform sentiment analysis using an external API
    sentiment_data = {'text': text}
    response = requests.post(f"{api_url}/predict", json=sentiment_data)
    if response.status_code == 200:
        result = response.json()
        negative_score = float(result.get("negative", 0))
        # Determine sentiment based on polarity
        if negative_score is None:
            sentiment = "Unknown"
        elif negative_score > 50:
            sentiment = "Negative"
        elif negative_score < 0:
            sentiment = "Positive"
        else:
            sentiment = "Neutral"
        return sentiment
    else:
        return "Unknown"

def process_csv(csv_file):
    app = create_app()  # Create Flask application instance
    with app.app_context():  # Create application context
        with open(csv_file, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                text = row['text']
                sentiment = analyze_sentiment(text)
                # Create and save the post with sentiment
                title=""
                hashtag=""
                user=1
                post = Post(title=title, hashtag=hashtag, content=text, sentiment=sentiment, user_id=user)
                db.session.add(post)
                time.sleep(2)
                db.session.commit()
    

if __name__ == "__main__":
    csv_file_path = "modified_dataset.csv"  # Replace with your CSV file path
    process_csv(csv_file_path)
