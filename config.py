# config.py
import os
from dotenv import load_dotenv

# Load variables from .env into the environment
load_dotenv()

# def get_kaggle_api_auth():
#     """
#     Fetch an API key from environment variables. Raises ValueError if the API key is not found

#     Args:
#         None

#     Returns:
#         dict: authorization HTTP header
#     """
#     key = os.getenv("NEWS_API_KEY")
#     if key is None:
#         raise ValueError("API key for 'NEWS_API_KEY' not found.")

#     return {"Authorization": key}


def get_reddit_api_auth():
    """
    Fetch an API key from environment variables. Raises ValueError if the API key is not found

    Args:
        None

    Returns:
        dict: client ID and client secret for Reddit API
    """
    client_id = os.getenv("REDDIT_CLIENT_ID")
    client_secret = os.getenv("REDDIT_CLIENT_SECRET")

    if client_id is None or client_secret is None:
        raise ValueError("Credentials for Reddit API 'REDDIT_CLIENT_ID' or 'REDDIT_CLIENT_SECRET' not found.")

    return {"client_id": client_id, "client_secret": client_secret}