# FinalProject_visualize.py
# For PART 3 of FinalProjectInstructions, or part 5 of the GradingScript

import os 
import sqlite3
import csv
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from finalproj import setup_db

def count_reddit_posts(cur):
    '''
    Counts the number of Reddit posts containing each of the song names in the Music table, 
    and writes the results to a CSV file.

    ARGUMENTS:
        cur: cursor object
    RETURNS:
        None
    '''

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


def visualize_spotify_mentions_ordered(cur, filename):
    '''
    Visualizes the Reddit mentions ordered by Spotify daily ranking in a bar chart
    by reading calculated data from a file. On the x-axis, the songs are ordered ascending by their
    daily_rank. 

    ARGUMENTS:
        cur: cursor object
        filename: the name of file to read data from 
    RETURNS:
        None
    '''

    # {song1: mentions1, song2: mentions2, ...}
    song_to_mentions = {}

    # Build the dictionary by reading the CSV file
    dir = os.path.dirname(__file__)
    with open(os.path.join(dir, filename)) as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            song_to_mentions[row[0]] = int(row[1])

    # Get song names and daily ranks from the database
    cur.execute('''
        SELECT Music.name, KaggleData.daily_rank
        FROM Music
        JOIN KaggleData ON Music.id = KaggleData.music_id
    ''')
    rows = cur.fetchall()
    
    # Build a list of lists [[daily_rank1, song_name1, mentions1], ...] to sort on daily_rank
    combined = []
    for song_name, daily_rank in rows:
        mentions = song_to_mentions.get(song_name, 0)  # mention == 0 if not found
        combined.append([daily_rank, song_name, mentions])

    combined_sorted = sorted(combined, key=lambda x: x[0])  # sorting by daily_rank, ascending

    sorted_ranks = []
    sorted_names = []
    sorted_mentions = []
    for item in combined_sorted:
        sorted_ranks.append(item[0])
        sorted_names.append(item[1])
        sorted_mentions.append(item[2])

    plt.figure(figsize=(16,8))
    plt.bar(sorted_names, sorted_mentions)
    plt.xlabel("Songs (Ordered by Spotify Daily Rank)")
    plt.ylabel("Number of Reddit Mentions")
    plt.title("Reddit Mentions by Spotify Daily Rank")
    plt.xticks(rotation=90)
    plt.show()


def visualize_top10_reddit_mentions(filename):
    '''
    Visualizes the top 10 songs by Reddit mention counts by reading from the csv file
    that stores the song names and their mention counts with Matplotlib 
    (counts of posts containing the song name).

    ARGUMENTS:
        filename: the name of the csv file containing song names and mention counts
    RETURNS:
        None
    '''

    # To store the song names and mention counts from CSV file
    song_name = []
    mention_count = []

    dir = os.path.dirname(__file__)
    with open(os.path.join(dir, filename)) as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            song_name.append(row[0])
            mention_count.append(int(row[1]))

    # Get the top 10 songs with the most mentions
    top_10_songs = song_name[:10]
    top_10_mentions = mention_count[:10]

    plt.figure(figsize=(10, 6))
    plt.barh(top_10_songs, top_10_mentions)
    plt.xlabel("Number of Reddit Mentions")
    plt.title("Top 10 Songs by Reddit Mentions")
    plt.show()

def visualize_ranking_c1_vs_c2_common(cur):
    """
    Visualizes the differences of music rankings between the US and Canada as an overlaid scatter plot. 

    ARGUMENTS:
        cur: cursor object
    RETURNS:
        None
    """

    # Get Country 1 data
    cur.execute("""
        SELECT Music.name, KaggleData.daily_rank, Country.name FROM KaggleData 
        JOIN Music ON KaggleData.music_id = Music.id
        JOIN Country ON KaggleData.country_id = Country.id
        WHERE KaggleData.country_id = 1
    """)

    c1_data = cur.fetchall()

    # Get Country 2 data
    cur.execute("""
        SELECT Music.name, KaggleData.daily_rank, Country.name FROM KaggleData 
        JOIN Music ON KaggleData.music_id = Music.id
        JOIN Country ON KaggleData.country_id = Country.id
        WHERE KaggleData.country_id = 2
    """)

    c2_data = cur.fetchall()

    c1_dict = {}
    c2_dict = {}

    for i in range(len(c1_data)):
        c1_dict[c1_data[i][0]] = c1_data[i][1]
    
    for i in range(len(c2_data)):
        c2_dict[c2_data[i][0]] = c2_data[i][1]

    c1_name = c1_data[0][2]
    c2_name = c2_data[0][2]
    

    # Create a figure
    plt.figure(figsize=(10, 6))

    # Plot the songs common to both countries
    common_songs = set(c1_dict.keys()) & set(c2_dict.keys())
    for song in common_songs:
        plt.scatter(song, c1_dict[song], color='blue', label=c1_name if song == next(iter(common_songs)) else "", s=100)
        plt.scatter(song, c2_dict[song], color='red', label=c2_name if song == next(iter(common_songs)) else "", s=100)

    # Plot the songs only in US
    # us_only_songs = set(us_dict.keys()) - set(ca_dict.keys())
    # for song in us_only_songs:
    #     plt.scatter(song, us_dict[song], color='blue', s=100)

    # # Plot the songs only in Canada
    # ca_only_songs = set(ca_dict.keys()) - set(us_dict.keys())
    # for song in ca_only_songs:
    #     plt.scatter(song, ca_dict[song], color='red', s=100)

    # Set labels and title
    plt.xlabel('Song Name')
    plt.ylabel('Ranking')
    plt.title(f'Ranking Comparison Between {c1_name} and {c2_name}')


    plt.ylim(0, 50)  # Set y-axis range from 1 to 50
    plt.yticks(np.concatenate(([1], np.arange(5, 56, 5))))  # Set ticks at multiples of 5

    # Invert y-axis to have 1 at the top
    plt.gca().invert_yaxis()

    # Add legend for the countries
    plt.legend()

    # Rotate x-axis labels for better visibility
    plt.xticks(rotation=90)


    # Display the plot
    plt.tight_layout()
    plt.show()
    
def visualize_spotify_popularity_vs_reddit_countries(cur):
    '''
    Visualizes the Spotify popularity v.s. Reddit mention counts as a scatter plot
    by reading data from the database. Differentiates by country.

    ARGUMENTS:
        cur: cursor object
    RETURNS:
        None
    '''

    # popularity = []
    # mention_count = []

    country_data = {}

    cur.execute('''
        SELECT Country.name, Music.name, KaggleData.popularity, COUNT(Reddit.id) as mention_count
        FROM Music
        JOIN Reddit ON Music.id = Reddit.music_id
        JOIN KaggleData ON Music.id = KaggleData.music_id
        JOIN Country ON KaggleData.country_id = Country.id
        GROUP BY Country.name, Music.name
    ''')
    rows = cur.fetchall()
    
    for row in rows:
        country_name = row[0]
        popularity = row[2]
        mention_count = row[3]
        if country_name not in country_data:
            country_data[country_name] = {"popularity": [], "mention_count": []}
        country_data[country_name]["popularity"].append(popularity)
        country_data[country_name]["mention_count"].append(mention_count)
    
    plt.figure(figsize=(10, 6))
    for country_name, data in country_data.items():
        plt.scatter(data["popularity"], data["mention_count"], alpha=0.3, edgecolors='black', label=country_name)

    plt.xlabel("Spotify Popularity")
    plt.ylabel("Reddit Mention Count")
    plt.title("Spotify Popularity vs Reddit Mention Count")
    plt.legend(country_data.keys())
    plt.grid()
    plt.tight_layout()
    plt.show()


def visualize_spotify_popularity_vs_reddit(cur):
    '''
    Visualizes the Spotify popularity v.s. Reddit mention counts as a scatter plot
    by reading data from the database.

    ARGUMENTS:
        cur: cursor object
    RETURNS:
        None
    '''

    popularity = []
    mention_count = []

    cur.execute('''
        SELECT Music.name, KaggleData.popularity, COUNT(Reddit.id) as mention_count
        FROM Music
        JOIN Reddit ON Music.id = Reddit.music_id
        JOIN KaggleData ON Music.id = KaggleData.music_id
        GROUP BY Music.name
    ''')
    rows = cur.fetchall()
    
    for row in rows:
        popularity.append(row[1])
        mention_count.append(row[2])
    
    plt.figure(figsize=(10, 6))
    plt.scatter(popularity, mention_count)
    plt.xlabel("Spotify Popularity")
    plt.ylabel("Reddit Mention Count")
    plt.title("Spotify Popularity vs Reddit Mention Count")
    plt.grid()
    plt.show()


def visualize_spotify_ranking_vs_reddit(cur):
    '''
    Visualizes the Spotify ranking v.s. Reddit mention counts as a bar chart
    by reading data from the database.

    ARGUMENTS:
        cur: cursor object
    RETURNS:
        None
    '''

    daily_ranks = []
    mentions = []

    cur.execute('''
        SELECT KaggleData.daily_rank, COUNT(Reddit.id)
        FROM Music
        JOIN Reddit ON Music.id = Reddit.music_id
        JOIN KaggleData ON Music.id = KaggleData.music_id
        GROUP BY Music.id
        ''')
    rows = cur.fetchall()

    for row in rows:
        daily_ranks.append(row[0])
        mentions.append(row[1])

    daily_ranks = sorted(daily_ranks, reverse=True)

    plt.figure(figsize=(10,6))
    plt.scatter(daily_ranks, mentions)
    # plt.gca().invert_xaxis()  # Rank 1 on the left
    plt.xlabel("Spotify Daily Rank (ascending)")
    plt.ylabel("Reddit Mentions")
    plt.title("Spotify Daily Rank vs Reddit Mentions")
    plt.grid(True)
    plt.show()


def main():

    print("===================================================================================")
    print("SI 206 W25 Final Project")
    print("Music trend analysis with Kaggle and Reddit API - DATA VISUALIZATION")
    print("===================================================================================\n")

    # Set up database
    db_name = "final.db"
    cur, conn = setup_db(db_name)

    # get Reddit post counts for each song
    count_reddit_posts(cur)

    filename = "reddit_post_counts.csv"

    options = '''Options:
    1. Option 1: Spotify Daily Rank - Country 1 vs. Country 2 (common songs)
    2. Option 2: Spotify Daily Rank (ascending) vs. Reddit Mention Frequency (bar)
    3. Option 3: Spotify Popularity vs. Reddit Mention Frequency
    4. Option 4: Spotify Daily Rank (ascending) vs. Reddit Mention Frequency (scatter)
    5. Option 5: Spotify Popularity (country 1 and country 2) vs. Reddit Mention Frequency
    6. Option 6: Top 10 Songs by Reddit Mentions
    8. Option 7: Everything
    8. Exit\n'''
    
    print(options)

    option = 0

    while option != 8: 
        option = int(input("\nPlease select an option (1-8): "))
        if option == 1:
            print("\nOption 1: Spotify Daily Rank - Country 1 vs. Country 2 (common songs)")
            visualize_ranking_c1_vs_c2_common(cur)
        elif option == 2:
            print("\nOption 2: Spotify Daily Rank (ascending) vs. Reddit Mention Frequency (bar)")
            visualize_spotify_mentions_ordered(cur, filename)
        elif option == 3:
            print("\nOption 3: Spotify Popularity vs. Reddit Mention Frequency")
            visualize_spotify_popularity_vs_reddit(cur)
        elif option == 4:
            print("\nOption 4: Spotify Daily Rank (ascending) vs. Reddit Mention Frequency (scatter)")
            visualize_spotify_ranking_vs_reddit(cur)
        elif option == 5:
            print("\nOption 5: Spotify Popularity (country 1 and country 2) vs. Reddit Mention Frequency")
            visualize_spotify_popularity_vs_reddit_countries(cur)
        elif option == 6:
            print("\nOption 6: Top 10 Songs by Reddit Mentions")
            visualize_top10_reddit_mentions(filename)
        elif option == 7:
            print("Everything")
            visualize_ranking_c1_vs_c2_common(cur)
            visualize_spotify_mentions_ordered(cur, filename)
            visualize_spotify_popularity_vs_reddit(cur)
            visualize_spotify_ranking_vs_reddit(cur)
            visualize_spotify_popularity_vs_reddit_countries(cur)
            visualize_top10_reddit_mentions(filename)
        elif option == 8:
            print("Exiting the program...")
        else:
            print("\nINVALID OPTION\n")    

    conn.close()


if __name__ == "__main__":
    main()