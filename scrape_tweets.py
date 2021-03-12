import csv
import twitterscraper
import datetime as dt
import sys
import re

def scrapingTweets(since,until):
    """
    Scrapes Tweets within a date range and writes them to a csv file. Scrapes Tweet text, Tweet ID, and Timestamp
    :param since: When you want to start. Should be in YYYY-MM-DD format.
    :param until: When you want to stop. Should be in YYYY-MM-DD format.
    :return: Filename of csv with tweets scraped
    """
    # upper bound and lower bound of queries. sometimes it is necessary to rescrape certain dates because twitter will start blocking your queries
    startDate = dt.datetime.strptime(since, '%Y-%m-%d').date()
    endDate = dt.datetime.strptime(until, '%Y-%m-%d').date()

    scraped_tweets_filename = "Coachella" + startDate.strftime("%Y" + "-" + "%m" + "-" + "%d") + "_" + endDate.strftime(
        ("%Y" + "-" + "%m" + "-" + "%d"))
    # queries tweets and writes each tweet to file
    collected_tweets = twitterscraper.query_tweets("Scraped Coachella Tweets", limit=None, begindate=startDate, enddate=endDate)
    with open(scraped_tweets_filename, 'w') as file:
        for tweet in collected_tweets:
            tweet_writer = csv.writer(file, delimiter=';', quoting=csv.QUOTE_ALL)
            tweet_writer.writerow(
                [tweet.id, tweet.timestamp.strftime("%m/%d/%Y %H:%M:%S"), tweet.text.replace('\n', ' '), tweet.user])


if __name__ == "__main__":

    # You will first have to have a list of the things you're looking for along with the associated regular expression(s)
    # artists = pd.read_csv("Artist_names.csv")

    try:
        args = sys.argv[1:]
        if len(args) != 2:
            raise ValueError("Please provide exactly 2 dates")
        date = re.compile('^\d{4}-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])$')
        for arg in args:
            if date.match(arg):
                pass
            else:
                raise ValueError("Dates are not the correct format! Please make sure they are YYYY-MM-DD")

        # Some more sanitization
        since = dt.datetime.strptime(args[0], '%Y-%m-%d').date()
        until = dt.datetime.strptime(args[1], '%Y-%m-%d').date()
        # Tweets can't go before this date
        if since < dt.date(2006,3,1):
            raise ValueError("Date is too early")
        # Can't get tweets from the future
        if until > dt.datetime.now().date():
            raise ValueError("Date is too late")

    except ValueError as error:
        print(error)
        sys.exit(1)

    # Arguments here for the date ranges are set manually. If certain dates are missing, simply rerun the scraper
    # for those dates and join the missing tweets to the file before continuing. Comment this out if you are using
    # the given data set and plug in the filename for the scraped tweets

    # '2019-01-03', '2019-05-03'
    scrapingTweets(*args)


