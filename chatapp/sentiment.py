from nltk.sentiment import SentimentIntensityAnalyzer

# Initialize the Sentiment Intensity Analyzer
sia = SentimentIntensityAnalyzer()

def analyze_sentiment(message):
    """
    Analyzes the sentiment of a given message using NLTK's VADER.
    Returns a sentiment polarity score between -1 (negative) and 1 (positive).
    """
    sentiment_scores = sia.polarity_scores(message)
    return sentiment_scores['compound']  # Return the compound sentiment score
