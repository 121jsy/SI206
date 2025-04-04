# config.py
import os
from dotenv import load_dotenv

# Load variables from .env into the environment
load_dotenv()

def get_api_key(api_name: str) -> str:
    """
    Fetch an API key from environment variables. Raises ValueError if the API key is not found

    Args:
        api_name (str): variable name in .env file (e.g., 'NEWS_API_KEY')

    Returns:
        dict: authorization HTTP header
    """
    key = os.getenv(api_name)
    if key is None:
        raise ValueError(f"API key for '{api_name}' not found.")
    return key

def get_news_api_key():
    return {"Authorization": get_api_key("NEWS_API_KEY")}

def get_pytrends_api_key() -> str:
    return {"Authorization": get_api_key("PYTRENDS_API_KEY")}