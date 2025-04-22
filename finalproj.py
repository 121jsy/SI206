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
    - How does the Reddit mention frequency of the most popular songs reflect that of Spotify, the 
      most pouplar music streaming platform?
    - Does Reddit mention frequency correlate with Spotify's daily ranking?
    - Does the Reddit mention frequency tell us something about the characteristics of Reddit?

APIs Used:
    - Kaggle API (kagglehub)
    - Reddit API (PRAW)

Visualization Tools:
    - Matplotlib
'''


import os
import sqlite3
import json
from datetime import datetime, timedelta
import time

import config

# APIs
import praw
import kagglehub
from kagglehub import KaggleDatasetAdapter

# Using OAuth to increase rate limit
reddit = praw.Reddit(
    client_id=config.REDDIT_CLIENT_ID,
    client_secret=config.REDDIT_CLIENT_SECRET,
    user_agent=config.REDDIT_USER_AGENT
)

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

    # Load Kaggle dataset into dataframe python object
    df = kagglehub.dataset_load(
        KaggleDatasetAdapter.PANDAS,
        "asaniczka/top-spotify-songs-in-73-countries-daily-updated",
        "universal_top_spotify_songs.csv",
        pandas_kwargs={"usecols": ["name", "artists", "daily_rank", "country", "snapshot_date", "popularity"]}
    )

    if df is not None:

        print("Dataset loaded successfully.\n")

        # Filter the dataframe based on criteria
        filtered_df = df
        for criteria_key, criteria_val in criteria.items():
            filtered_df = filtered_df.loc[(filtered_df[criteria_key] == criteria_val)]

        # TESTING - display whole dataset
        print(filtered_df)
        print()

        # Option 1: Convert the dataset to JSON (for project's purpose) format and keep as a python object
        if option == "1":
            print("Option 1 (default): Saving dataset as json format python object")
            json_string = filtered_df.to_json(orient='records', lines=False)
            json_object = json.loads(json_string)

            return json_object

        # Option 2: Convert the dataset to JSON format (for project's purpose) and save it in the current directory.
        #           For testing and viewing data contents
        elif option == "2":
            filtered_df.to_json(os.path.join(current_directory, 'universal_top_spotify_songs.json'), 
                    orient='records', 
                    lines=False)
            
    else:
        print("Failed to load dataset.\n")


def setup_db(db_name):
    '''
    Sets up and connects to the SQLite database in local directory and returns
    cursor and connection objects.

    ARGUMENTS:
        db_name: database filename
    RETURNS:
        cur: cursor object
        conn: connection object
    '''
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + "/" + db_name)
    cur = conn.cursor()
    return cur, conn


def create_update_kaggle_db(cur, conn, json_object=None):
    '''
    Creates the KaggleData table in the SQLite database and inserts/updates it with the 
    JSON data retrieved with Kagglehub API. 
    
    ARGUMENTS:
        cur: cursor object
        conn: connection object
        json_object (dict): A dictionary containing the data retrieved with Kaggle API
    RETURNS:
        cur: cursor object
        conn: connection object
    '''

    # Create Music table (unique music name and id)
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Music (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE
        )
    ''')
    # Create KaggleData table (linked to Music table with FOREIGN KEY)
    cur.execute('''
        CREATE TABLE IF NOT EXISTS KaggleData (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            music_id INTEGER,
            country_id INTEGER,
            daily_rank INTEGER,
            popularity INTEGER,
            FOREIGN KEY (country_id) REFERENCES Country(id),
            FOREIGN KEY (music_id) REFERENCES Music(id)
            UNIQUE (music_id, country_id) 
        )
    ''') #UNIQUE (music_id, country_id) doesn't allow to insert a row with existing music_id AND country_id -> music_id는 같은데 country_id 다른 경우는 ok

    #Create Country Table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Country (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT
        )
    ''')

    # Insert the data into the Music table and KaggleData table
    if json_object is not None:
        count = 0
        for music in json_object:
            if count >= 25:
                conn.commit()
                return cur, conn
            
            name = music["name"]
            country = music["country"]

            # To avoid inconsistent id, check if song exists in the Music table
            # Without this step, the "id" will be skipped (e.g. 24, 25, 51, 52, ...)
            cur.execute("SELECT id FROM Music WHERE name = ?", (name,))
            row = cur.fetchone()
            if row is None: #insert the data if not there
                cur.execute("INSERT OR IGNORE INTO Music (name) VALUES (?)", (name,))
                music_id = cur.lastrowid
            else:
                music_id = row[0]

            #Get Country id or insert the data to Country table
            cur.execute("SELECT id FROM Country WHERE name = ?", (country,))
            row = cur.fetchone()
            if row is None: #insert the data if not there
                cur.execute("INSERT OR IGNORE INTO Country (name) VALUES (?)", (country,))
                country_id = cur.lastrowid
            else:
                country_id = row[0]
            
            # Get the corresponding music_id from the Music table
            # cur.execute("SELECT id FROM Music WHERE name = ?", (name,))
            # music_id = cur.fetchone()[0] -->위 코드랑 겹치는 거 같음
            # Insert the rest of the data into the KaggleData table
            daily_rank = music["daily_rank"]
            popularity = music["popularity"]

            cur.execute("INSERT OR IGNORE INTO KaggleData (music_id, country_id, daily_rank, popularity) VALUES (?, ?, ?, ?)",
                        (music_id, country_id, daily_rank, popularity))
            
            if cur.rowcount == 1:   # rowcount property returns the affected by the previous execute()
                count += 1          # Thus, if the affected (newly inserted) row is 1, increment count

    conn.commit()
    return cur, conn

            
def create_update_reddit_db(cur, conn, post_dict):
    '''
    Creates the Reddit table in the SQLite database and inserts/updates it with the 
    data from the song_post_dict, which is a dictionary containing song names as keys and 
    lists of Reddit posts as values. Updates the table with 25 or less rows each call.

    ARGUMENTS:
        cur: cursor object
        conn: connection object
        song_post_dict (dict): A dictionary containing song names as keys and lists of Reddit posts as values
    RETURNS:
        cur: cursor object
        conn: connection object
    '''
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Reddit (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE,
            music_id INTEGER,
            FOREIGN KEY (music_id) REFERENCES Music(id)
        )
    ''')

    count = 0

    for music_name, posts in post_dict.items():
        for post in posts: #list of post dictionaries
            if count >= 25:
                conn.commit()
                return cur, conn
            cur.execute("SELECT id FROM Music WHERE name = ?", (music_name,))
            music_id = cur.fetchone()[0]
            cur.execute("INSERT OR IGNORE INTO Reddit (title, music_id) VALUES (?, ?)",
                        (post['title'], music_id))
            if cur.rowcount == 1:   # rowcount property returns the affected by the previous execute()
                count += 1          # Thus, if the affected (newly inserted) row is 1, increment count

    conn.commit()
    return cur, conn


def search_reddit_posts(cur):
    """
    Groups up the song names from the Music table and calls group_search() to search
    Reddit posts containing the song names. Groups 5 songs together per Reddit API 
    .search() method to increase request efficiency. 

    ARGUMENTS:
        cur: cursor object
    RETURNS:
        song_posts (dict): A dictionary where keys are song names and values are lists of Reddit posts
        containing those song names in titles or texts. Each key-value pair is returned from group_search().
    """

    # {"song_name1": [{post1 data}, {post2 data}, ...], "song_name2": [{post1}, {post2}, ...], ...}
    song_posts = {}

    grouping_size = 5   # Number of songs to group for efficient search
    cur.execute("SELECT name FROM Music")   
    songs = [row[0] for row in cur.fetchall()] #list of music names from MUSIC table
    total_songs = len(songs)

    # Increase the start_index by +grouping_size (5) each time, until it reaches total_songs (100)
    # 61 songs in Music table
    # Updates the grouped_songs list with 5 songs each time
    for start_index in range(0, total_songs, grouping_size):
        grouped_songs = [] # ["song_name1", "song_name2", ..., "song_name5"]
        end_index = min(start_index + grouping_size, total_songs)  # avoid IndexError

        for i in range(start_index, end_index):
            grouped_songs.append(songs[i])

        group_search_results = group_search(grouped_songs)

        for song_name, posts in group_search_results.items():
            song_posts[song_name] = posts

        time.sleep(0.6)

    return song_posts


def group_search(song_names, max_posts=100):
    """
    Searches for the top Reddit posts from the past month mentioning each song name 
    in the specified list of subreddits. Groups up the subreddit names to increase request efficiency.

    ARGUMENTS:
        song_names (list): A list of song names to search for.
        max_posts (int): The maximum number of posts to retrieve.
    RETURNS:
        posts_by_song (dict): A dictionary where keys are song names and values are lists of Reddit posts
        containing those song names in titles or texts.
    """
    # Group up the subreddits to search in
    subreddit_group = "Music+hiphopheads+popheads+popculturechat"
    # '"song1" OR "song2" OR ... OR "song5"'
    query = " OR ".join([f'"{name}"' for name in song_names])

    # Prepopulated dictionary 
    # {"song_name1": [{post1 data}, {post2 data}, ...], "song_name2": [{post1}, {post2}, ...], ...}
    posts_by_song = {}
    for name in song_names:
        posts_by_song[name] = []

    subreddit = reddit.subreddit(subreddit_group)
    # Search for posts in the chosen subreddits
    for post in subreddit.search(query, sort="top", time_filter="month", limit=max_posts):
        # Text of the title and selftext of the post (lowercased for proper match count)
        text = (post.title + " " + post.selftext).lower()

        # Check if the post contains the music name. If so, insert into dictionary
        for song in song_names:
            if song.lower() in text:
                post_data = {
                    "id": post.id,
                    "title": post.title,
                }
                posts_by_song[song].append(post_data)

    return posts_by_song

def main():
    # ========================================================================================
    print("\n===================================================================================")
    print("SI 206 W25 Final Project")
    print("Music trend analysis with Kaggle and Reddit API -  DATA RETRIEVAL / DATABASE SETUP")
    print("===================================================================================\n")
    # print("--------------------------------------------------------")
    # print("-----------------------------------------------------------------------------------\n")

    date = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')
    
    print("NOTE: Program is designed to run multiple times using a loop to retrieve data from Kaggle and Reddit.\n")

    print("-----------------------------------------------------------------------------------")
    print("Step 1: Load Kaggle dataset and set up database")
    print("-----------------------------------------------------------------------------------\n")

    load_options = '''Kaggle dataset loading options:
    1: python object
    2: local json file\n'''
    print(load_options)

    load_option = input("Please select an option (1 or 2): ")
    print()

    country1 = input("First country to search for: ")
    country2 = input("Second country to search for: ")

    criteria = {
        "country": country1,
        "snapshot_date": date
    }
    c1_json_object = load_kaggle_dataset(criteria, load_option)

    criteria = {
        "country": country2,
        "snapshot_date": date
    }
    c2_json_object = load_kaggle_dataset(criteria, load_option)

    # Groups up the US and CA JSON data to pass into create_update_kaggle_db()
    json_object = c1_json_object + c2_json_object

    # Sets up the database
    cur, conn = setup_db("final.db")

    # Updates tables associated with Kaggle with the JSON data at most 25 items each time
    for count in range(25, 101, 25):
        proceed = input("Enter [o] to update database (Kaggle): ")
        if proceed == "o":
            print(f"Update KaggleData table with 25 items. (Total: {count} items)")
            cur, conn = create_update_kaggle_db(cur, conn, json_object)

    
    print("\n-----------------------------------------------------------------------------------")
    print("Step 2: Search Reddit posts and update database")
    print("-----------------------------------------------------------------------------------\n")

    print("Searching Reddit Posts...\n")
    song_post_dict = search_reddit_posts(cur) #fetched post data

    print("Program is designed to run multiple times using a loop to retrieve data from Kaggle and Reddit.")
    print("\t[o]: to start updating database.")
    print("\t[x]: to stop database updates and exit the program.")

    option = ""
    count = 1
    while option != "x":
        option = input("[o] update / [x] stop: ")
        if option == "o":
            cur, conn = create_update_reddit_db(cur, conn, song_post_dict)
            print(f"Updated Reddit table {count} times. Check Reddit table each time.")
            count += 1
        if option == "x":
            print("Ending Reddit database updates\n")

    conn.close()

        
    '''
    main() IMPLEMENTATION WITHOUT LOOPS

    print("-----------------------------------------------------------------------------------")
    print("Step 1: Load Kaggle dataset and set up database")
    print("-----------------------------------------------------------------------------------\n")

    load_options = "Kaggle dataset loading options:\n1: python object\n2: local json file\n"
    print(load_options)

    load_option = input("Please select an option (1 or 2): ")
    print()

    country1 = input("First country to search for: ")
    country2 = input("Second country to search for: ")

    criteria = {
        "country": country1,
        "snapshot_date": date
    }
    c1_json_object = load_kaggle_dataset(criteria, load_option)

    criteria = {
        "country": country2,
        "snapshot_date": date
    }
    c2_json_object = load_kaggle_dataset(criteria, load_option)

    # Groups up the US and CA JSON data to pass into create_update_kaggle_db()
    json_object = c1_json_object + c2_json_object

    # Sets up the database
    cur, conn = setup_db("final.db")

    cur, conn = create_update_kaggle_db(cur, conn, json_object)

    print("\n-----------------------------------------------------------------------------------")
    print("Step 2: Search Reddit posts and update database")
    print("-----------------------------------------------------------------------------------\n")

    print("Searching Reddit Posts...\n")
    song_post_dict = search_reddit_posts(cur) #fetched post data

    cur, conn = create_update_reddit_db(cur, conn, song_post_dict)

    conn.close()
    '''

if __name__ == "__main__":
    main()

