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

import os
import sqlite3
import json
import pandas as pd
import requests

import kagglehub
from kagglehub import KaggleDatasetAdapter

# kagglehub.login()

def load_kaggle_dataset(option="1"):
    '''
    Loads kaggle dataset (Top Spotify Songs in 73 Countries (Daily Updated)) using Kaggle public API.
    Saves the dataset in the current directory as a .json file, or stores it as a python object 
    depending on user choice.

    ARGUMENTS:
        option (str): An optional argument that indicates the loading/saving option.

    RETURNS:
        json_object: A dataset in json format returned with option=1. 
        None: Returned with option=2. json file saved in current directory
    '''

    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Load Kaggle dataset into python object
    df = kagglehub.dataset_load(
        KaggleDatasetAdapter.PANDAS,
        "asaniczka/top-spotify-songs-in-73-countries-daily-updated",
        "universal_top_spotify_songs.csv"
    )

    if df is not None:
        # Option 1: Convert the dataset to .json (for project's purpose) format and keep as a python object
        if option == "1":
            print("Option 1 (default): Saving dataset as json format python object")
            json_string = df.to_json(orient='records', lines=False)
            json_object = json.loads(json_string)
            
            update_database(data=json_object)

            # return json_object

        # Option 2: Convert the dataset to .json format (for project's purpose) and save it in the current directory
        elif option == "2":
            df.to_json(os.path.join(current_directory, 'universal_top_spotify_songs.json'), 
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


def search_reddit_data():
    # TODO: Decide whether to use Reddit API or PRAW, and implement the search function
    # Also consider how to store the data into database: each music gets mention frequency 
    # data or store them intoseparate table
    pass


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
    json_object = load_kaggle_dataset(load_option)

    if json_object is not None:
        pass


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
            keyword = input("Keyword/phrase to search for: ")
            # param = {
            #     "language": "en",
            #     "category": "general",
            #     "from": "2025-01-01",
            #     "to": "2025-04-01",
            #     "q": keyword,
            # }

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






