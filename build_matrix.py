import pandas as pd
import numpy as np
import itertools
import re
import time
import csv
from os import path
import sys

def matchArtistInTweets(artists_regex_filename, scraped_tweets_filename):
    """
    Finds matches of artist within tweets given a list of artist, writes all artists found to a csv file. Passes on TypeError or ValueError.
    :param artists_regex_filename: Filename of a csv containing on each row a regex pattern followed by what it represents
    :param scraped_tweets_filename: Filename of csv containing Tweets to find matches in.
    :return: Returns the filename of the csv file of artists found within the scraped Tweets.
    """

    df = pd.read_csv(scraped_tweets_filename, sep=';', encoding='utf-8', engine='python')
    artists = pd.read_csv(artists_regex_filename)
    results = []

    #timimg for how long this will take
    start_time = time.time()

    #For each artist name matched, add it to a list of matches.
    for index, tweet in df.iterrows():
        list_of_matches = []
        for row in artists.iterrows():
            regex = row[1][0]
            compiled_regex = re.compile(regex, flags=re.IGNORECASE)
            try:
                tweet_text = tweet['Text']
                if re.search(compiled_regex, tweet_text):
                    artist_name = row[1][1]
                    list_of_matches.append(artist_name)
            except ValueError:
                pass
            except TypeError:
                pass
        results.append(list_of_matches)
        #Displays how many tweets have been processed, per thousand
        if index % 1000 == 0:
            print("%d Tweets have been processed!" % index)

    #For all the artists that are matched in the list, we take only the ones that have two or more artists matched.

    finished_results = []

    for i in results:
        if len(i) > 1:
            finished_results.append(i)

    #writes to file
    matched_artists_filename = "Matched" + scraped_tweets_filename.strip("Scraped")
    with open(matched_artists_filename, "w") as f:
        writer = csv.writer(f)
        writer.writerows(finished_results)

    print("This took: %d seconds" % (time.time() - start_time))

    return matched_artists_filename


def createMatrix(artists_regex_filename, matched_artists_filename):
    """
    Creates an adjacency matrix of artist co-mentions, weights them, and writes to a file called "relationship_matrix.csv".
    :param artists_regex_filename: Filename of a csv containing on each row a regex pattern followed by what it represents
    :param matched_artists_filename: Filename of all artists found within a list of Tweets.
    :return: N/A
    """
# Takes from a pre-made list of strings to be matched as regular expressions.
# Probably better to do this in a dictionary rather than a nest list (?)
    # TODO : Rewrite to not use pandas...What were you thinking?
    artists = pd.read_csv(artists_regex_filename)
    list_of_artists = artists['Name'].tolist()

#making an adjacency matrix to add to since we know how many artists there are.
    matrix_of_artists = np.zeros((list_of_artists.len(), list_of_artists.len()))

    with open(matched_artists_filename) as f:
        lines = f.read().splitlines()

    for mentioned_artists in lines:
        artists_in_tweet = mentioned_artists.split(',')

#getting rid of tweets that mention only the headliners, because these tweets are not interesting to us
        if not (len(artists_in_tweet) == 3 and 'Childish Gambino' in artists_in_tweet
                and 'Ariana Grande' in artists_in_tweet and 'Tame Impala' in artists_in_tweet):

#each permutation within a tweet represents a linkage. append to the matrix for each one found.
            edges_in_tweet = itertools.permutations(artists_in_tweet, 2)
            for edge in edges_in_tweet:
                index_of_artist_one = list_of_artists.index(edge[0])
                index_of_artist_two = list_of_artists.index(edge[1])
                matrix_of_artists[index_of_artist_one][index_of_artist_two] += 1
    print(matrix_of_artists)

# here I am going to weight the tweets. More popular artists will obviously get more tweets.
# This presents some problems with co-mentions as some co-mentions might be overrepresented.
# One solution is to divide each co-mention (twice) by the total number of co-mentions each artist has. This
# will (hopefully) make sure the matrix accurately reflects the association between artists relative to the total
# number of co-mentions for each artist regardless of how popular they are. This is (somewhat) similar to td-idf.

    df_matrix = pd.DataFrame(data=matrix_of_artists[0:, 0:], index=list_of_artists[0:], columns=list_of_artists[0:])
    df_matrix["sum"] = df_matrix.sum(axis=1)
    df_matrix_weighted = df_matrix.loc[:, "Childish Gambino": "Tara Brooks"].div(matrix_of_artists["sum"], axis=0)
    df_matrix_weighted = df_matrix_weighted.loc[:, "Childish Gambino": "Tara Brooks"].div(matrix_of_artists["sum"], axis=1)

# write to csv

    df_matrix_weighted.to_csv("relationship_matrix.csv")


if __name__ == "__main__":

    # You will first have to have a list of the things you're looking for along with the associated regular expression(s)
    try:
        if not path.exists('Artist_names.csv'):
            raise FileNotFoundError("You need Artist_names.csv in this directory")
    except FileNotFoundError as error:
        print(error)
        sys.exit(1)

    artists = pd.read_csv("Artist_names.csv")

    try:
        scraped_tweets_filename = sys.argv[1]
        if not path.exists(scraped_tweets_filename):
            raise FileNotFoundError("File of scraped tweets not found")
    except FileNotFoundError as error:
        print(error)
        sys.exit(1)
    except IndexError:
        print("Need to provide exactly one argument!")
        sys.exit(1)

    matched_artists_filename = matchArtistInTweets(artists, scraped_tweets_filename)

    createMatrix(artists, matched_artists_filename)
