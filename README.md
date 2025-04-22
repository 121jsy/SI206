# SI 206 Winter 2025 Final Project

---

## Project: APIs, SQL, and Visualizations

### Team Members:
- Joonseo Yoon / joonseoy
- Shea Shin / yoonseos

---

## References
- Kaggle API (kagglehub): https://github.com/Kaggle/kagglehub?tab=readme-ov-file#user-content-fn-2-e8c07f4a8c03b71229d22ad6a451a240
- Reddit API: https://www.reddit.com/dev/api/
- Reddit API PRAW: https://praw.readthedocs.io/en/stable/

---

## Project Description
Uses Kaggle API to retrieve "Top Spotify Songs in 73 Countries" dataset and Reddit API to observe  
the popularity of the songs reflected on one of the most popular social media, Reddit.

---

## Questions
- How does the Reddit mention frequency of the most popular songs reflect that of Spotify, the most popular music streaming platform?
- Does Reddit mention frequency correlate with Spotify's daily ranking?
- Does the Reddit mention frequency tell us something about the characteristics of Reddit?

---

## APIs Used
- Kaggle API (kagglehub)
- Reddit API (PRAW)

---

## Visualization Tools
- Matplotlib

---

## Instructions for Running the Program

### `finalproj.py`: Program for retrieving data from Kaggle using Kagglehub and Reddit using Reddit API PRAW. Creates and updates the SQLite database.
1. Run the program
2. The program will prompt the user for Kaggle dataset loading options. Choose 1 for loading the dataset into a JSON Python object or choose 2 to save it as a local JSON file. Option 2 is used for testing and viewing the contents of the dataset, so for this project, select option 1.
3. Enter the first ISO 3166-1 alpha-2 (i.e., two-letter country code). For our project demonstration, we are using “US”
4. Enter the second ISO 3166-1 alpha-2 (i.e., two-letter country code). For our project demonstration, we are using “CA”
5. Enter “o” to update the database with the Kaggle dataset with 25 items. Repeat four times. With each iteration, check the “KaggleData” table in “final.db” SQLite database to confirm that the table was updated.
6. Enter “o” to update the database with Reddit post data with no more than 25 items. Repeat this a few times while checking the “Reddit” table for each iteration. If the iteration does not update the table anymore, enter “x” to stop updating.

### `FinalProject_visualize.py`: Program to visualize the collected data.
1. Run the program
2. View and enter an option from the visualization options.
3. View the visualization, then close the Matplotlib visualization to return to the program
4. Repeat until desired. Enter “8” to exit the program.

---
