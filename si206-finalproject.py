'''
Project: SI 206 Winter 2025 Project, APIs, SQL, and Visualizations
Team Members:
    - Joonseo Yoon / joonseoy
    - Shea Shin / yoonseos
References (Generative AI, Websites, etc.):
    - ChatGPT:
        - Common practice for storing and accessing API keys in main program. Stored API keys in
          .env file and used dotenv library to retrieve them in a helper file, config.py.
        - Common practice for making HTTP requests using "params" parameter in .get() method.
          Implemented passing API keys via the Authorization HTTP header. 

Project Description:
    To answer the question "How well do the different news sources cover the trending topics, 
    and how frequently are their articles shared?", we will use the pytrends and NewsAPI APIs to
    gather various data on trending topics and news articles. The data will be stored in the
    SQLite database and analyzed to obtain visualizations on the correlation between the two, 
    such as "news coverage on trending topics by news sources", "trend overlap and news coverage", 
    "geographic news coverage map", and so on. 

APIs Used:
    - pytrends [https://github.com/GeneralMills/pytrends]
    - NewsAPI (https://newsapi.org/docs)
    Alternatives:
        - SerpAPI Google Trends API [https://serpapi.com/, 100 searches / month]
        - TheNewsAPI [https://www.thenewsapi.com/, 100 requests / day]
        - GNewsAPI [https://gnews.io/, 100 requests / day, 10 articles / request]

Visualization Tools:
    - Plotly
    - Pandas
'''

import requests
import json
import unittest
import os
import sqlite3
import datetime
# import api_keys
import pandas as pd   

from config import get_news_api_auth_header
from pytrends.request import TrendReq


def get_trend_data(request_param):
    '''
    Fetches trending topics from pytrends API

    ARGUMENTS: 
        pytrends_key (str): API key for pytrends
        request_param (dict): Search parameter for pytrends API 
                              (https://pypi.org/project/pytrends/#common-api-parameters)
                              kw_list: list of keywords to get data for 
                                       (e.g. ["k1", "k2", "k3", "k4", "k5"])
                              cat: category id to narrow results (e.g. '71')
                              tz: timezone offset in minutes (e.g. '360')
                              timeframe: date to start from, defaults to last 5 yrs ('today 5-y')
                                         (e.g. 'all', '2023-12-14 2024-12-25', ...)
                              gprop: Google property ('images', 'news', 'youtube', 'froogle')

    RETURNS: 
        
    '''

    pass
    


def get_news_data_everything(request_param):
    '''
    Fetches every articles within given parameters from NewsAPI

    ARGUMENTS: 
        request_param (dict): Search parameter for pytrends API (https://newsapi.org/docs/endpoints/everything)
                              q: keywords of a phrase to search for
                              searchIn: the fields to restrict the q search to (title,description,content)
                              sources: comma-separated string of identifiers for the news sources/blogs
                              domains: comma-separated string of domains to restrict the search to
                              excludeDomains: comma-separated string of domains to remove from the results
                              from: date and time to start the search from (YYYY-MM-DDTHH:MM:SSZ)
                              to: ISO 8601 format date and optional time for the oldest article allowed
                              language: 2-letter ISO-639-1 code of the language to get headlines for
                              sortBy: relevancy, popularity, publishedAt (default)
                              pageSize: number of results to return per page request (100 default, 100 max)
                              page: use this to page through the results (1 default)

    RETURNS: 
        articles (list): List of news articles related to the trending topics
    '''



    base_url = "https://newsapi.org/v2/everything"
    headers = get_news_api_auth_header()

    response = requests.get(base_url, headers=headers, params=request_param)

    if response.status_code == 200:
        data = response.json()
        update_newsapi_database("newsapi", "everything", request_param, data)
    else:
        print(f"Failed to retrieve data \nstatus_code: {response.status_code}\n response text: {response.text}\n")
        return None


def get_news_headlines(request_param):
    '''
    Fetches news headlines within the given parameters from NewsAPI

    ARGUMENTS: 
        request_param (dict): Search parameter for pytrends API (https://newsapi.org/docs/endpoints/top-headlines)
                              country: 2-letter ISO 3166-1 country code (e.g. "us", "kr", "ua")
                              category: headline category (e.g. "business", "entertainment")
                              sources: comma-separated string of identifiers for the news sources/blogs
                              q: keywords of a phrase to search for
                              pageSize: number of results to return per page request (20 default, 100 max)
                              page: page to use if the total results found is greater than the page size
    '''
    

def get_news_sources(request_param):
    '''
    Fetches every available news sources information from NewsAPI within the given parameters

    ARGUMENTS:
        search_param (dict): Search parameter for NewsAPI API (https://newsapi.org/docs/)
                            category: headline category (e.g. "business", "entertainment")
                            language: 2-letter code for language (e.g. "eg", "de", "fr")
                            country: 2-letter ISO 3166-1 country code (e.g. "us", "kr", "ua")
    
    RETURNS:
        None
    '''
    # url = f"https://newsapi.org/v2/top-headlines/sources?apiKey={newsapi_key}"

    
def update_newsapi_database(api_name, endpoint, request_param, data):
    '''
    Updates the corresponding NewsAPI SQL database with the data fetched from the APIs, based on
    the data type. If the database does not exist, create a new one. If the database exists, update 
    the existing database with the new data, without duplicate entries.

    ARGUMENTS:
        api_name (str): name of the API used to fetch the data (e.g. "pytrends", "newsapi")
        endpoint (str): name of the data with different request parameters 
                        (e.g. "interest_over_time", "interest_by_region", "trending_searches"
                        "everything", "top-headlines", ...)
        request_param (dict): name of the data with different request parameters 
                              (e.g. "interest_over_time", "interest_by_region", "trending_searches", 
                              "q": , )
        data (list): list of data to be inserted into the database
        
    RETURNS:
        None
    '''
    
    dir_path = os.path.dirname(os.path.realpath(__file__))

    # Create a string of request parameters to be used in the database name
    # e.g. "country=us&category=sports&sources=cnn,bbc-news,fox-news"
    param = ""
    for param_key, param_val in request_param:
        param += f"{param_key}={param_val}&"
    param = param[:-1]  # remove the last '&' character

    filename = f"{dir_path}/{api_name}_{endpoint}_{request_param}.sqlite"

    # Create a new SQL database if file does not exist already
    if not os.path.isfile(filename):
        conn = sqlite3.connect(filename)
        cur = conn.cursor()

        # Create new pytrends table
        # !!!NEEDS FURTHER IMPLEMENTATION!!! Since there are a wide range of request parameter combinations
        # and we cannot cover all of them in one table nor make sqlite files for every single one of them,
        # we need to choose which ones to actually get for this project.
        if api_name == "pytrends":
            cur.execute('''
                CREATE TABLE IF NOT EXISTS pytrends (
                    id INTEGER PRIMARY KEY,
                    keyword TEXT,
                    date TEXT,
                    interest INTEGER
                )
            ''')
        # Create new newsapi table
        # !!!NEEDS FURTHER IMPLEMENTATION!!! Since there are a wide range of request parameter combinations
        # and we cannot cover all of them in one table nor make sqlite files for every single one of them,
        # we need to choose which ones to actually get for this project.
        elif api_name == "newsapi":
            if data_type == "everything":
                cur.execute('''
                    CREATE TABLE IF NOT EXISTS newsapi (
                        id INTEGER PRIMARY KEY,
                        title TEXT,
                        description TEXT,
                        url TEXT,
                        publishedAt TEXT,
                        source TEXT
                    )
                ''')

        # Insert data into the table
        for row in data:
            cur.execute('''
                INSERT OR IGNORE INTO newsapi (title, description, url, publishedAt, source)
                VALUES (?, ?, ?, ?, ?)
            ''', (row['title'], row['description'], row['url'], row['publishedAt'], row['source']))
        
        conn.commit()
        conn.close()
        




    # EXAMPLE:
    dir_path = os.path.dirname(os.path.realpath(__file__))

    filename = dir_path + '/' + "cache.json"

    with open('movies.txt', 'r') as f: 
        movies = f.readlines()
        
    for i in range(len(movies)): 
        movies[i] = movies[i].strip()
    movies = movies

    # NOTE: if you already have a cache file, setUp will open it
    # otherwise, it will cache all movies to use that in the test cases 
    if not os.path.isfile(filename):
        cache = update_cache(movies, 'cache.json')
    else:
        cache = get_json_content(filename)

    url = "http://www.omdbapi.com/"




def main():

    pytrends = TrendReq(hl='en-US', tz=360)
    # pytrends = TrendReq(retries=3)

    # pytrends.build_payload(kw_list=['Korea'], timeframe=['2025-01-01 2025-04-01'])
    df = pytrends.top_charts(date=2024, hl='en-US', tz=360, geo='US')

    print(df.to_string())


    # newsapi_key = get_news_api_auth_header()
    # pytrends_key = get_pytrends_api_key()
    # ========================================================================================
    print("===================================================================================")
    print("SI 206 W25 Final Project")
    print("Data Analysis with NewAPI and Pytrends")
    print("===================================================================================\n")
    # print("--------------------------------------------------------")
    # print("-----------------------------------------------------------------------------------\n")

    options = '''Options:
    1. News coverage on trending topics by news sources
    2. Trend vs. article frequency over time for a keyword
    3. Trend overlap and news coverage
    4. Geographic news coverage map by trend category
    5. News coverage by trend category
    6. All above
    7. Exit\n'''
    
    print(options)

    option = 0

    while option != "7":
        # get user input
        option = input("Please select an option (1-7): ")
        print()

        if option == "1":
            print("Option 1: News coverage on trending topics by news sources\n")
            trending_topics = get_trend_data("trending_searches")
            # param = {
            #     "language": "en",
            #     "category": "general",
            #     "from": "2025-01-01",
            #     "to": "2025-04-01",
            #     "apiKey": newsapi_key
            # }
            # get_news_data_everything(param)

        elif option == "2":
            print("Option 2: Trend vs. article frequency over time for a keyword\n")
        elif option == "3":
            print("Option 3: Trend overlap and news coverage\n")
        elif option == "4":
            print("Option 4: Geographic news coverage map by trend category\n")
        elif option == "5":
            print("Option 5: News coverage by trend category\n")
        elif option == "6":
            print("Option 6: All above\n")
        elif option == "7":
            print("Exiting the program...\n")
            return
        else:
            print("INVALID OPTION\n")
            print(options)

        print("-----------------------------------------------------------------------------------\n")


    # You can now pass these keys to API clients
    # e.g., requests.get("...", headers={"Authorization": news_key})

if __name__ == "__main__":
    main()