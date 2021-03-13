# Twitter-Coachella-Grouping
Visualize groupings of musical artists based on artist co-mentions within a tweet

## BACKGROUND

This project uses a simple series of scripts to farm Tweets about Coachella, analyze them, and visualize them.

Artist co-mentions are collected into an adjacecny matrix. A community detection algorithm (Louvain) is then used in order to group artists, and they are visualized using visNetwork. 

This is a very basic way to visualize insights, if any, on the way people talk about musical artists, such as (hopefully) what artists are considered "similar" or are liked similarly by Twitter users.

I tried to write the code here in such a way that it should be a simple task to do the same for just about any other topic of your choosing. All you should need are a list of things you're looking for within your tweets and a working knowledge of Regular Expression. 

This is my first (!!) coding project I have ever done (very exciting!!). If you have any resources you should want to point me to, tips or tricks on how to better code, or any further projects, please do not hesitate to contact me as I would be most grateful for feedback of any kind.

Below is an example of the kind of Tweets we are farming for:
>**@tuhleequh**
>
>ARIANA GRANDE • LOS TUCANES • THE 1975 • BILLIE EILLISH • YG • DVSN 
>brb literally crying over the #coachella lineup 😭😭😭
>
>8:39 PM - 2 Jan 2019

This is an example of the "ideal" tweet we are looking for. The user is excited about several artists announced in the lineup, which is great!

The assumption is that if a person likes a few artists, it's at least a little bit likely that these artists will be similar. 

Of course, we are not asserting that famed Mexican norteño band [Los Tucanes de Tijuana](https://en.wikipedia.org/wiki/Los_Tucanes_de_Tijuana) is the same as [Ariana Grande](https://en.wikipedia.org/wiki/Ariana_Grande), but there is at least one person who likes them both. This in itself is fairly interesting to look at. 

There are some similarities to be found in [how music recommendation algorithms recommend musical artists to you](https://medium.com/datadriveninvestor/behind-spotify-recommendation-engine-a9b5a27a935).

Obviously, this project is not as complicated as performing collaborative filtering to recommend artists, but it is, nonetheless, a fun way to see the opinions of people and the way they talk about musical artists.

### ASSUMPTIONS

There are a few more assumptions that you'll have to accept as true:

1. **When people tweet about artists, they like both of them.**

   So a tweet like this:
   >**@CoachellaH8ter2000**
   >
   >I am so excited for Ariana Grande but would hate to see Childish Gambino.
   >
   >9:99 AM - 32 Jab 2291
   
   would spell disaster. Currently [Twitter's REST API](https://developer.twitter.com/en/docs/tweets/rules-and-filtering/overview/standard-operators) provides you with ways to search for only positive tweets so that we can avoid that nasty negativity, but there are certain limitations to using the official API.<sup>1</sup> Without the official API (or letting go of Tweets that couldn't _reliably_ be deemed positive), I would have to perform some [sentiment analysis and NLP](https://en.wikipedia.org/wiki/Sentiment_analysis) on these Tweets, which is quite difficult!. 

2. **When people tweet about artists, it is about the music.**

   So a tweet like this:
   >**@CoachellaOutfitt3r4000**
   >
   >I love Beyoncé's outfits and I cannot believe Idris Elba is totally copying her style.
   >
   >89:87 PM - 55 Fob 1127
   
   would be catastraphoic. Musical artists often stir up drama with each other. This muddles the picture.

3. **When people tweet about artists, they are not simply retweeting news articles.**

   So a tweet like this:
   >**@CoachellaR3porter6000**
   >
   >Tame Impala, Ariana Grande, and Childish Gambino to headline Coachella. Read more through our paywall.
   >
   >29:00 FM 99 Ran 3301
   
   would be devastation. I have tried to correct for this by manually removing, any Tweets that mention the headliners (and only the headliners), but there are obvious limitations to this method. 
   
4. **When people tweet about artists, they are not using any nicknames that I haven't thought of.**

   So a tweet like this (really, who does this?):
   >**@CoachellaLuvr8000**
   >
   >I am so excited to see Tame Imp. and Åriånå Grånde.
   >
   >89:87 PM - 55 Mon 1127
   
   would be cruel. And needlessly make me write more Regex. 

...and so on. More assumptions can be specified, but generally they are reconfigurations of:

_If and only if people tweet about artists, they like the music._

### AUTHOR'S DISCLAIMER

**_It is not the intent of the author to damage, harm, or otherwise distress any persons, but the author recognizes that written within this repository is code  that is potentially damaging, harmful, or distressful to mental health, most especially if the reader should have any expertise in object-oriented programming or mathematics beyond a high-school level._**

_<sup>1</sup> Without a Premium or Enterprise account, Twitter provides access only to the last 7 days of Tweets since the current date, while limiting the number of Tweets returned per request to 180 on a user request. This is decidedly not a good thing if you do not have the patience to scrape Tweets every week for five months or cannot afford to drop the [$1900](https://developer.twitter.com/en/docs/tweets/search/overview/premium) on a Premium Developer account to get 1 million tweets._ 

_It is slightly more economical (free) to scrape the front-end._ 

## THE PROCESS

### OVERVIEW
I farmed around 870k Tweets that reference Coachella using [taspinar's](https://github.com/taspinar) [twitterscraper](https://github.com/taspinar/twitterscraper) and sorted through them to find any mentions of all of the musical artists within the lineup.

To install twitterscraper run:

```pip3 install twitterscraper```

To run the scraper, simply run the `scrape_tweets.py` script with your desired beginning and end dates in that order, e.g.:

```python3 scrape_tweets.py 2019-01-03 2019-05-03```

#### UPDATE: As of March 2021, most/all scrapers now no longer work, including twitterscraper. 

Tweets were collected in the time period between 2019-01-03 (when the Coachella line-up was first announced) to four months after, 2019-05-03.

Scraped tweets are provided in a ZIP file. 

A file of all of the artist names and their corresponding regexes are also needed to scrape the tweets and build the adjacency matrix of the weighted graph. This is also provided. 

I used Python to create an adjacency matrix that is weighted by how often the artist was mentioned in a style similar to td-idf. 

To build the adjcency matrix that you need to load into visNetwork, run the `build_matrix.py` script with the filename of the scraped tweets, e.g.:

```python3 build_matrix.py All_tweets_semi```

I then import the adjacency matrix into an R session, create an igraph object from the matrix, and render a visNetwork object from the igraph object.

This code can be pretty easily rewritten to match any topic and any "things" that you want to see connected. For example, we can substitute out Coachella for Cheese and have artist names be names of cheeses. The world is your oyster!


MANY thanks to:

(http://www.shizukalab.com/toolkits/sna/sna_data)

(https://www.jessesadler.com/post/network-analysis-with-r/)

(https://kateto.net/network-visualization)

(https://rpubs.com/mfwade)

