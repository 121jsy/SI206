# config.py
import os
from dotenv import load_dotenv

# Load variables from .env into the environment
load_dotenv()

def get_news_api_auth_header():
    """
    Fetch an API key from environment variables. Raises ValueError if the API key is not found

    Args:
        None

    Returns:
        dict: authorization HTTP header
    """
    key = os.getenv("NEWS_API_KEY")
    if key is None:
        raise ValueError("API key for 'NEWS_API_KEY' not found.")

    return {"Authorization": key}


def get_tweepy_api_auth():
    """
    Fetch an API key from environment variables. Raises ValueError if the API key is not found

    Args:
        None

    Returns:
        dict: authorization HTTP header
    """
    consumer_key = os.getenv("TWEEPY_CONSUMER_KEY")
    consumer_secret = os.getenv("TWEEPY_CONSUMER_SECRET")
    access_token = os.getenv("TWEEPY_ACCESS_TOKEN")
    access_token_secret = os.getenv("TWEEPY_ACCESS_TOKEN_SECRET")

    

    if key is None:
        raise ValueError("API key for 'NEWS_API_KEY' not found.")

    return {"Authorization": key}

# def get_pytrends_api_key() -> str:
#     return {"Authorization": get_api_key("PYTRENDS_API_KEY")}