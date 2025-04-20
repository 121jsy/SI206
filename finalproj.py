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
import csv

import config

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

        # Option 1: Convert the dataset to .json (for project's purpose) format and keep as a python object
        if option == "1":
            print("Option 1 (default): Saving dataset as json format python object")
            json_string = filtered_df.to_json(orient='records', lines=False)
            json_object = json.loads(json_string)

            # create_update_kaggle_db(json_object)

            return json_object

        # Option 2: Convert the dataset to .json format (for project's purpose) and save it in the current directory
        elif option == "2":
            filtered_df.to_json(os.path.join(current_directory, 'universal_top_spotify_songs.json'), 
                    orient='records', 
                    lines=False)
            
            update_database(filename='universal_top_spotify_songs.json')
    else:
        print("Failed to load dataset.\n")



'''
기존에 안쓰이던 function 업데이트: Music table (id, unique music name), KaggleData table (잡다한 정보+ Music table의 
id foreign key로 reference) 생성. 나중에 고려해야 될 것들: 
1. KaggleData table의 id, music_id, daily_rank가 다 똑같음
2. country, snapshot_date column에 있는 값들 다 똑같음
3. snapshot_date는 아예 없애고, country는 새로운 table을 만들고 foreign key로 reference하는게 어떨지? -> 해결
'''
def create_update_kaggle_db(cur, conn, json_object=None):
    '''
    Updates the database SQLite database with the json data or filename. If the data is
    provided, it will insert the data directly into the database. If the filename is provided,
    it will read the file and insert the data into the database.

    ARGUMENTS:
        json_object (dict): A dictionary containing the data retrieved with Kaggle API
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

"""
나중에 DB 다 완성되면 쓸 function
Count reddit posts containing specific keyword in title or text by selecting data from Reddit DB
"""
def count_reddit_posts(cur):

    # Step 1: Get all distinct Music.id and Music.name
    cur.execute("SELECT id, name FROM Music")
    music_rows = cur.fetchall()  # [(1, 'NOKIA'), (2, 'luther'), ...]

    result = [("name", "count")]

    # Step 2: For each music entry in Music table, use JOIN to count matching Reddit posts
    for music_id, music_name in music_rows:
        cur.execute('''
            SELECT COUNT(Reddit.id)
            FROM Reddit
            JOIN Music ON Reddit.music_id = Music.id
            WHERE Music.id = ?
        ''', (music_id,))
        count = cur.fetchone()[0]
        result.append((music_name, count))

    # Step 3: Sort results by count DESC (excluding header first)
    result_body = sorted(result[1:], key=lambda x: x[1], reverse=True)
    result_sorted = [result[0]] + result_body

    # Step 4: Write to CSV
    current_directory = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(current_directory, "reddit_post_counts.csv")
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(result_sorted)


   
    
"""
Set up database in local directory and returns cursor and connection objects
"""
def setup_db(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + "/" + db_name)
    cur = conn.cursor()
    return cur, conn
            
"""
Create Reddit database using passed cursor and connection objects
It stores less than 25 items each time it's called and makes sure there's no duplicates -> 이건 아직 모르겠음
25 개씩 넣는 logic 약간 수정, Music table에 있는 id를 reference 해서 삽입
"""
def create_update_reddit_db(cur, conn, post_dict):
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

'''
Reddit OAuth랑 PRAW사용해서 rate limit 늘리고 data retrieval efficiency 최대한 늘린 버전
1. search_reddit_posts() 에서는 json_data를 받고, 그걸 읽어서 노래를 5개씩 묶은 리스트를 만든 후, group_search()에 넘겨줌
2. group_search()에서는 노래 제목들을 받고, subreddit을 그루핑 한 후 그 그룹의 subreddit에서 검색, 그 결과를 다시 search_reddit_posts()에 넘겨줌
3. group_search()에서 리턴된 결과를 search_reddit_posts()이 받으면 song_posts에 업데이트 하는 방식
'''
def search_reddit_posts_v1(cur):
    """
    Retrieves Reddit posts mentioning each song in the provided JSON data.
    Groups 5 songs together per Reddit API search to be more efficient.
    """

    # {"song_name1": [{post1 data}, {post2 data}, ...], "song_name2": [{post1}, {post2}, ...], ...}
    song_posts = {}

    grouping_size = 5   # Number of songs to group for efficient search
    cur.execute("SELECT name FROM Music")   
    songs = [row[0] for row in cur.fetchall()] #list of music names from MUSIC table
    total_songs = len(songs)

    # Increase the start_index by +grouping_size (5) each time, until it reaches total_songs (100) --> music table에 있는 모든 노래는 61개로 들어가있음
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
    Searches for Reddit posts containing the group of song names in the chosen subreddit group. 
    Seaches from the top posts of past month.

    ARGUMENTS:
        song_names (list): A list of song names to search for.
        max_posts (int): The maximum number of posts to retrieve.
    RETURNS:
        posts_by_song (dict): A dictionary where keys are song names and values are lists of Reddit posts
        containing those song names.
    """
    # Group up the subreddits to search in
    subreddit_group = "Music+hiphopheads+popheads+popculturechat"
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


"""
새로 수정한 function
Search reddit posts containing specific keyword
It does not count the number of posts, but just returns the dictionary with fetched data. -> update the dictionary
key는 keyword(i.e. music name)이고 keyword 당 모든 subreddit에서 matching된 post data를 저장한 list를 value로 함
"""
def search_reddit_posts(keyword, post_dict, max_posts_per_sub=400):
    headers = {
        "User-Agent": "KeywordTracker/1.0 by si206final"
    }
    data_list = []
    subreddits = ["popheads", "Music", "hiphopheads", "popculturechat"] #popular music relevant subreddits

    for sub in subreddits:
        print(f"\n🔍 Searching r/{sub} for keyword: '{keyword}'...")
        after = None
        fetched = 0
        count = 0

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

            if not children: #no posts
                break

            for child in children:
                post = child["data"]
                # Check keyword in title or text
                if keyword.lower() in (post.get("title", "").lower() + " " + post.get("selftext", "").lower()):
                    data_list.append(post)
                    count += 1

            fetched += len(children)
            after = data.get("after") #to get more than 100 results
            #If after is None or missing, that means: You've reached the last page of results.

            if not after:
                break

            time.sleep(2)  # avoid rate-limiting 
        print(f"✅ Found {count} matching posts in r/{sub}")    
    # print(f"data list size is {len(data_list)}")
    post_dict[keyword] = data_list # ex) {"NOKIA" : [{post1}, {post2}, {post3} ... ] }
    return post_dict

"""
Search reddit posts in past month that contain specific keyword in title or text.
It returns the total count of posts
"""
# def search_reddit_posts(keyword, max_posts_per_sub=400):
#     headers = {
#         "User-Agent": "KeywordTracker/1.0 by si206final"
#     }

#     all_results = {}
#     total_count = 0

#     '''
#     for (all kaggle json data):
#         if (the song critera chosen == true (e.g. [song1, song2, ..., song25]))
            
#     '''
#     subreddits = ["popheads", "Music", "hiphopheads", "popculturechat"] #popular music relevant subreddits

#     for sub in subreddits:
#         print(f"\n🔍 Searching r/{sub} for keyword: '{keyword}'...")
#         posts = []
#         after = None
#         fetched = 0

#         while fetched < max_posts_per_sub:
#             url = f"https://www.reddit.com/r/{sub}/search.json"
#             params = {
#                 "q": keyword,
#                 "restrict_sr": "on", #only search in the subreddit
#                 "sort": "top",
#                 "t": "month",
#                 "limit": 100, #number of items to fetch
#             }
#             if after:
#                 params["after"] = after

#             response = requests.get(url, headers=headers, params=params)
#             if response.status_code != 200:
#                 print(f"Error fetching from r/{sub}: {response.status_code}")
#                 break

#             data = response.json().get("data", {})
#             children = data.get("children", [])

#             if not children:
#                 break

#             for child in children:
#                 post = child["data"]
#                 # Check keyword in title or text
#                 if keyword.lower() in (post.get("title", "").lower() + " " + post.get("selftext", "").lower()):
#                     posts.append(post)

#             fetched += len(children)
#             after = data.get("after") #to get more than 100 results
#             #If after is None or missing, that means: You've reached the last page of results.

#             if not after:
#                 break

#             time.sleep(2)  # avoid rate-limiting

#         print(f"✅ Found {len(posts)} matching posts in r/{sub}")
#         total_count += len(posts)
#         all_results[sub] = posts
    
#     return total_count

# def filter_by_date(posts, start_date, end_date):
#     """
#     Filters posts to only include those within the date range.
#     start_date and end_date should be in 'YYYY-MM-DD' format.
#     """
#     start_ts = int(time.mktime(datetime.strptime(start_date, "%Y-%m-%d").timetuple()))
#     end_ts = int(time.mktime(datetime.strptime(end_date, "%Y-%m-%d").timetuple()))

#     filtered = []
#     for post in posts:
#         post_time = post.get("created_utc")
#         if post_time and start_ts <= post_time <= end_ts:
#             filtered.append(post)
#     return filtered



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
            us_json_object = load_kaggle_dataset(criteria, load_option)
            criteria = {
                "country": "CA",
                "snapshot_date": "2025-04-18"
            }
            ca_json_object = load_kaggle_dataset(criteria, load_option)

            json_object = us_json_object + ca_json_object # us data랑 ca data 하나로 묶어서 create_update_kaggle_db() function에 넘겨줌

            # 
            cur, conn = setup_db("final.db") #Final DB 만들기
            print("Create and update Kaggle table with 25 items")
            cur, conn = create_update_kaggle_db(cur, conn, json_object)
            option = input("Enter anything to load more items to the Kaggle table ")
            cur, conn = create_update_kaggle_db(cur, conn, json_object)
            print("\nCheck now there are 50 items in the Kaggle DB")
            option = input("Enter anything to load more items to the Kaggle table ")
            cur, conn = create_update_kaggle_db(cur, conn, json_object)
            print("\nCheck now there are 75 items in the Kaggle DB")
            option = input("Enter anything to load more items to the Kaggle table ")
            cur, conn = create_update_kaggle_db(cur, conn, json_object)
            print("\nCheck now there are 100 items in the Kaggle DB")

            song_post_dict = search_reddit_posts_v1(cur) #fetched post data
            # print(f"it should be 61 and it is {len(song_post_dict)}")

            while(option != "exit"): #Reddit post 개수가 총 몇개 있을지 모르겠어서 일단 while true로 해놓음 -> 일단은 Reddit db 확인하면서 더이상 업데이트 안될때까지 해야함 (173 rows)
                cur, conn = create_update_reddit_db(cur, conn, song_post_dict) #Reddit DB update 
                option = input("Enter anything to load more items to the Reddit table, Check Reddit table each time ")

            #write a calculation result as a csv file
            count_reddit_posts(cur)


            """
            참고로 밑에 url 들어가면 api call 했을 때 어떤 식으로 json이 리턴되는지 바로 볼 수 있어.
            https://www.reddit.com/r/Music/search.json?q=NOKIA&restrict_sr=on&sort=top&t=month&limit=100

            -앞으로 더 해야할 것-
            1. Reddit table에 id INTEGER PRIMARY KEY AUTOINCREMENT 설정하기 -> 해결
            2. music_id DB 만들기 -> 지금 Reddit DB에 있는 duplicate string들을 int id 로 바꾸기 -> 해결
            3. 모든 노래에 대해서 Reddit db 업데이트 하기  -> 해결
            4. kaggle DB 만들기 -> 해결

            -directory 변경사항- 
            1. config.py에 REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT 넣기 <- 이건 내일 알려줄게

            -할거 추가!- 
            1. Duplicate String 추가 확인하기 (e.g. KaggleData에 music_id, daily_rank, country, snapshot_date 다 똑같음)
            2. 일자별 + 각 국가별 노래가 50개씩이라 "100 rows per API"아직 충족 못함 -> 다른 나라 노래 가져오는 것 고려 -> 캐나다 노래 50개 가져옴
                - 두 국가의 top 50에서 중복되는 노래가 있을 수 있는데, 노래 제목은 music_id로 바꿔서 저장하니까 redundant data는 딱히
                  걱정 안해도 될 듯. 추가로 Country table까지 만들어서 foreign key로 reference하면 같은 곡이어도 구분 가능 -> music_id와 country_id 둘다 동일하면 db에 안넣어지게 설정함. 그래서 같은 곡이라도 
                  country_id 가 다르면 db에 들어감, 둘 다 같으면 안들어감
            3. KaggleData에 100 rows 다 저장하면 mention count 구하기 -> 카운트 해서 csv 파일로 저장함
            4. setup_db() 내에서 create_update_kaggle_db() 및 create_update_reddit_db() 호출하기
                - 더 깔끔함. 이렇게 하려면 load_kaggle_dataset()에서 create_update_kaggle_db() 호출하지 말것
                - create_update_kaggle_db()에서 return 받은 값을 curr, conn이랑 같이 넘겨주는 방식? -> 일단은 각각 create_update_db() 부르는 방식으로 돼있음, 일단은 create_update_kaggle_db를 다 완료하고 
                그 다음에 create_update_reddit_db를 불러야 돼서 두 함수를 각각 따로 빼놓는게 좋을거 같기도..한데 잘은 모르겟어 아직..ㅎㅎ
            5. 코드 정리
            6. Calculation function들 작성
            7. Visualization function들 작성
            8. 리포트 작성
            """
                

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