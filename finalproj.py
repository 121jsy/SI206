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
    - https://stackoverflow.com/questions/4906977/how-can-i-access-environment-variables-in-python


Project Description:
    Uses Kaggle API to retrieve "Top Spotify Songs in 73 Countries" dataset and Reddit API to observe
    the popularity of the songs reflected on one of the most popular social media, Reddit.

Questions:
    - What is the best way to calculate the sentiment "score" of the articles? 
      (Just the headlines or the whole article? Or a combination of both? How do we calculate the score?)
    - Is the sentiment score accurate?
    - How do we visualize the results in a meaningful way?

APIs Used:
    - Kaggle API
    - Reddit API

Visualization Tools:
    - Plotly
    - Pandas
'''

import requests
import json
import unittest
import os
import sqlite3
import pandas as pd

# Have to resolve later
import kaggle
# from kaggle.api.kaggle_api_extended import KaggleApi
# from kagglehub import KaggleDatasetAdapter

file_path = ""

df = kagglehub.load_dataset(
  KaggleDatasetAdapter.PANDAS,
  "asaniczka/top-spotify-songs-in-73-countries-daily-updated",
  file_path,
)

print("First 5 records:", df.head())