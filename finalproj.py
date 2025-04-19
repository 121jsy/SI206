'''
Project: SI 206 Winter 2025 Project, APIs, SQL, and Visualizations
Team Members:
    - Joonseo Yoon / joonseoy
    - Shea Shin / yoonseos
References (Generative AI, Websites, etc.):
    - Kaggle API (kagglehub): https://github.com/Kaggle/kagglehub?tab=readme-ov-file#user-content-fn-2-e8c07f4a8c03b71229d22ad6a451a240
    - Reddit API: https://www.reddit.com/dev/api/
    - Reddit API PRAW: https://praw.readthedocs.io/en/stable/

Project Description:
    Uses Kaggle API to retrieve "Top Spotify Songs in 73 Countries" dataset and Reddit API to observe
    the popularity of the songs reflected on one of the most popular social media, Reddit.

Questions:
    - What is the best way to calculate the sentiment "score" of the articles? 
      (Just the headlines or the whole article? Or a combination of both? How do we calculate the score?)
    - Is the sentiment score accurate?
    - How do we visualize the results in a meaningful way?

APIs Used:
    - Kaggle API (kagglehub)
    - Reddit API (PRAW?)

Visualization Tools:
    - Plotly
    - Pandas
'''
import praw

import os
import sqlite3
import json
import pandas as pd
import requests
from datetime import datetime
import time

from config import get_reddit_api_auth

import kagglehub
from kagglehub import KaggleDatasetAdapter

# kagglehub.login()

def load_kaggle_dataset(criteria, option="1"):
    '''
    Loads kaggle dataset (Top Spotify Songs in 73 Countries (Daily Updated)) using Kaggle public API.
    Saves the dataset in the current directory as a .json file, or stores it as a python object 
    depending on user choice.

    ARGUMENTS:
        option (str): An optional argument that indicates the loading/saving option.
        criteria (dict): Argument that decides what data to keep (e.g. {"country": "US", "data_start": "2025-04-01"})

    RETURNS:
        json_object: A dataset in json format returned with option=1. 
        None: Returned with option=2. json file saved in current directory
    '''

    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Load Kaggle dataset into python object
    df = kagglehub.dataset_load(
        KaggleDatasetAdapter.PANDAS,
        "asaniczka/top-spotify-songs-in-73-countries-daily-updated",
        "universal_top_spotify_songs.csv",
        pandas_kwargs={"usecols": ["name", "artists", "daily_rank", "daily_movement", "weekly_movement", "country", "snapshot_date", "popularity"]}
    )

    # Check if the dataset is loaded successfully
    if df is not None:
        print("Dataset loaded successfully.")
        print(df.head(10))
        print(df.columns)
    else:
        print("Failed to load dataset.")
        return None

    # Filter the dataframe based on criteria
    filtered_df = df
    for criteria_key, criteria_val in criteria.items():
        filtered_df = filtered_df.loc[(filtered_df[criteria_key] == criteria_val)]
    
    # print(filtered_df)

    if filtered_df is not None:
        # Option 1: Convert the dataset to .json (for project's purpose) format and keep as a python object
        if option == "1":
            print("Option 1 (default): Saving dataset as json format python object")
            json_string = filtered_df.to_json(orient='records', lines=False)
            json_object = json.loads(json_string)
            # print(json_object)
            # update_database(data=json_object)

            return json_object

        # Option 2: Convert the dataset to .json format (for project's purpose) and save it in the current directory
        elif option == "2":
            filtered_df.to_json(os.path.join(current_directory, 'universal_top_spotify_songs.json'), 
                    orient='records', 
                    lines=False)
            
            update_database(filename='universal_top_spotify_songs.json')
    else:
        print("Failed to load dataset.")


def update_database(data=None, filename=None):
    '''
    Updates the database SQLite database with the json data or filename. If the data is
    provided, it will insert the data directly into the database. If the filename is provided,
    it will read the file and insert the data into the database.

    ARGUMENTS:
        data (list): A list of dictionaries containing the data to be inserted into the database.
        filename (str): The name of the json file containing the data to be inserted into the database.
    
    RETURNS:
        Bool: True if database is successfully updated, False otherwise.
    '''
    pass


# def search_reddit_data():
#     # TODO: Decide whether to use Reddit API or PRAW, and implement the search function
#     # Also consider how to store the data into database: each music gets mention frequency 
#     # data or store them intoseparate table
#     credentials = get_reddit_api_auth()
#     id = credentials['client_id']
#     secret = credentials['client_secret']
#     reddit = praw.Reddit(
#     client_id=id,
#     client_secret=secret,
#     user_agent='si206:v1.2.3 (by u/Grand_Compote2026)' )

#     # print(reddit.read_only)
#     # for submission in reddit.subreddit("music").hot(limit=10):
#     #     print(submission.title)

#     # subreddit = reddit.subreddit("music")
#     # keyword = "Sabrina Carpenter"
#     # count = 0
#     # for submission in subreddit.new(limit=100):  # or .hot/.top/.search etc.
#     #     if keyword.lower() in submission.title.lower() or keyword.lower() in submission.selftext.lower():
#     #         count += 1
#     # print(f"'{keyword}' mentioned in {count} recent posts on r/music")

#     # return count
#     subreddit = "music"
#     keyword = "Taylor Swift"
#     start_date = "2024-12-01"
#     end_date = "2025-04-01"
#     subreddit = reddit.subreddit("music")
#     start_ts = int(datetime.strptime(start_date, "%Y-%m-%d").timestamp())
#     end_ts = int(datetime.strptime(end_date, "%Y-%m-%d").timestamp())

#     count = 0
#     # for submission in subreddit.hot(time_filter="all"):
#     #     post_ts = int(submission.created_utc)
#     #     # if start_ts <= post_ts <= end_ts:
#     #     title = submission.title.lower()
#     #     body = submission.selftext.lower()
#     #     if keyword.lower() in title or keyword.lower() in body:
#     #         count += 1
#     #         print(submission.title)
#     # print(f"Found {count} posts mentioning '{keyword}' in r/{subreddit} between {start_date} and {end_date}.")

#     count = 0
#     keyword = "sabrina carpenter"
#     for submission in reddit.subreddit("Music+hiphopheads+popheads").top(time_filter="month"):
#         if keyword.lower() in submission.title.lower() or keyword.lower() in submission.selftext.lower():
#            count += 1
#            print(submission.title)
#            print(f"count : {count}")

#     return count
def count_reddit_posts(json_data):
    reddit_dict = {}
    for music in json_data:
        name = music["name"]
        post_count = search_reddit_posts(name)
        reddit_dict[name] = post_count
    
    return json.dumps(reddit_dict)
            



def search_reddit_posts(keyword, max_posts_per_sub=400):
    headers = {
        "User-Agent": "KeywordTracker/1.0 by si206final"
    }

    all_results = {}
    total_count = 0

    '''
    for (all kaggle json data):
        if (the song critera chosen == true (e.g. [song1, song2, ..., song25]))
            
    '''
    subreddits = ["popheads", "Music", "hiphopheads", "popculturechat"] #popular music relevant subreddits

    for sub in subreddits:
        print(f"\n🔍 Searching r/{sub} for keyword: '{keyword}'...")
        posts = []
        after = None
        fetched = 0

        while fetched < max_posts_per_sub:
            url = f"https://www.reddit.com/r/{sub}/search.json"
            params = {
                "q": keyword,
                "restrict_sr": "on", #only search in the subreddit
                "sort": "top",
                "t": "month",
                "limit": 100, #number of items to fetch
            }
            if after:
                params["after"] = after

            response = requests.get(url, headers=headers, params=params)
            if response.status_code != 200:
                print(f"Error fetching from r/{sub}: {response.status_code}")
                break

            data = response.json().get("data", {})
            children = data.get("children", [])

            if not children:
                break

            for child in children:
                post = child["data"]
                # Check keyword in title or text
                
                if keyword.lower() in (post.get("title", "").lower() + " " + post.get("selftext", "").lower()):
                    posts.append(post)

            fetched += len(children)
            after = data.get("after") #to get more than 100 results
            #If after is None or missing, that means: You've reached the last page of results.

            if not after:
                break

            time.sleep(1)  # avoid rate-limiting

        print(f"✅ Found {len(posts)} matching posts in r/{sub}")
        total_count += len(posts)
        all_results[sub] = posts
    
    return total_count

def filter_by_date(posts, start_date, end_date):
    """
    Filters posts to only include those within the date range.
    start_date and end_date should be in 'YYYY-MM-DD' format.
    """
    start_ts = int(time.mktime(datetime.strptime(start_date, "%Y-%m-%d").timetuple()))
    end_ts = int(time.mktime(datetime.strptime(end_date, "%Y-%m-%d").timetuple()))

    filtered = []
    for post in posts:
        post_time = post.get("created_utc")
        if post_time and start_ts <= post_time <= end_ts:
            filtered.append(post)
    return filtered


def update_kaggle_database(json_data):
    '''

    '''



def main():
    # ========================================================================================
    print("===================================================================================")
    print("SI 206 W25 Final Project")
    print("Music trend analysis with Kaggle and Reddit API")
    print("===================================================================================\n")
    # print("--------------------------------------------------------")
    # print("-----------------------------------------------------------------------------------\n")

    load_options = '''Dataset loading options:
    1: python object
    2: local json file\n'''
    print(load_options)

    load_option = input("Please select an option (1 or 2): ")
    print()

    options = '''Options:
    1. Option 1: Spotify Daily Rank vs. Reddit Mention Frequency
    2. Option 2: Spotify Popularity vs. Reddit Mention Frequency
    3. Option 3: Spotify Music's Artist vs. Reddit Mention Frequency
    4. Option 4: Explit Music Reddit Mention. Non-Explicit Music Reddit Mention
    5. Option 5: ??? Reddit Sentiment ??? (EC using additional API, e.g. TextBlob)
    6. Option 6: ???
    7. Exit\n'''
    
    print(options)

    option = 0

    while option != "7":
        # get user input
        option = input("Please select an option (1-7): ")
        print()

        if option == "1":
            print("Option 1: Top Charts \n")
            # keyword = input("Keyword/phrase to search for: ")
            criteria = {
                "country": "US",
                "snapshot_date": "2025-04-18"
            }
            json_object = load_kaggle_dataset(criteria, load_option)
            results = count_reddit_posts(json_object)

            total = 0
            print("\n📊 Summary:")
            for name, posts in results.items():
                print(f"{name} with {posts} posts")
                

        elif option == "2":
            print("Option 2: \n")
        elif option == "3":
            print("Option 3: \n")
        elif option == "4":
            print("Option 4: \n")
        elif option == "5":
            print("Option 5: \n")
        elif option == "6":
            print("Option 6: All above\n")
        elif option == "7":
            print("Exiting the program...\n")
            return
        else:
            print("INVALID OPTION\n")
            print(options)

        print("-----------------------------------------------------------------------------------\n")


# def main():
    # subreddits = ["popheads", "Music", "hiphopheads", "popculturechat"] #popular music relevant subreddits
    # keyword = "sza"

    # results = count_reddit_posts(json_object)


    # total = 0
    # print("\n📊 Summary:")
    # for sub, posts in results.items():
    #     print(f"r/{sub}: {len(posts)} posts")
    #     total += len(posts)
    # print(f"\n🎯 Total posts with '{keyword}': {total}")

    # print()
    # print('//////////Filter post date////////////')

    # filtered_results = {}
    # filtered_count = 0
    # for sub, posts in results.items():
    #     filtered_results[sub] = filter_by_date(posts, "2025-03-01", "2025-04-01")
    #     print(f"r/{sub}: {len(filtered_results[sub])} posts between Mar 2025 and Apr 2025")
    #     filtered_count += len(filtered_results[sub])
    
    # print(f"📊 Found {filtered_count} posts with '{keyword}' between Mar 2025 and Apr 2025")




if __name__ == "__main__":
    main()






'''
1. Choose the option 
2. Get all the data from kaggle and store it into json object
    - Manipulate data and insert into Kaggle database (25 song each)
3. Get all the reddit posts related to the option (~100 posts/request - repeat to get whole month's data)
    - Count all the mentions 
    - Insert the mention count into the json object 
4. Insert into Reddit database 25 each time (individual counts of ~25 songs)

Reference:
Aggregating subreddits: https://www.reddit.com/r/redditdev/comments/uwfrc7/the_rate_limit_of_60_requests_per_minute_might/
Increased Rate Limits: https://www.reddit.com/r/redditdev/comments/14nbw6g/updated_rate_limits_going_into_effect_over_the/
    Free API access rates are as follows:
        - 100 queries per minute per OAuth client id if you are using OAuth authentication
        - 10 queries per minute if you are not using OAuth authentication
PRAW Rate limit Headers: https://www.reddit.com/r/redditdev/comments/7muatr/praw_rate_limit_headers/


4/18
- Successfully filtered data from Kaggle (desired column and val in column)
    - 50 per country
TODO: Make an option "save only" to run at least four times 
    - Retrieve Kaggle data (maybe 2 countries?) and save it as json object
    - Retrieve Reddit data by reading the json object 
    - Store the data into database
'''