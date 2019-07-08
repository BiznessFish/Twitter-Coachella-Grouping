# Twitter-Coachella-Grouping
Visualize groupings of musical artists based on artist co-mentions within a tweet

## BACKGROUND

This project uses a simple series of scripts to farm Tweets about Coachella, analyze them, and visualize them.

Artist co-mentions are collected into an adjacecny matrix. A community detection algorithm is then used in order to group artists, and they are visualized using visNetwork. 

This is a very basic way to visualize insights, if any, on the way people talk about musical artists, such as (hopefully) what artists are considered "similar" or are liked similarly by Twitter users.

Below is an example:
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

Obviously, this project is nowhere near as complicated as performing collaborative filtering to recommend artists, but it is, nonetheless, a fun way to see the collective opinion of people and the way they talk about things.

### ASSUMPTIONS

There are a few more assumptions that you'll have to accept as true:

1. **When people tweet about artists, they like both of them.**

   So a tweet like this:
   >**@CoachellaH8ter2000**
   >
   >I am so excited for Ariana Grande but would hate to see Childish Gambino.
   >
   >9:99 AM - 32 Jab 2291
   
   would spell disaster. Currently [Twitter's REST API](https://developer.twitter.com/en/docs/tweets/rules-and-filtering/overview/standard-operators) provides you with ways to search for only positive tweets so that we can avoid that nasty negativity, but there are certain limitations to using the official API.<sup>1</sup> Without the official API (and missing Tweets that can't _reliably_ be deemed positive), I would have to perform [sentiment analysis and NLP](https://en.wikipedia.org/wiki/Sentiment_analysis) on these Tweets. Which is really hard. 

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

   So a tweet like this (really, who would do this?):
   >**@CoachellaLuvr8000**
   >
   >I am so excited to see Tame Imp. and Åriånå Grånde.
   >
   >89:87 PM - 55 Mon 1127
   
   would be cruel. And needlessly pushing my already poor understanding of Regular Expressions. 

...and so on. More assumptions can be specified, but generally they are reconfigurations of:

_If and only if people tweet about artists, they like the music._

### AUTHOR'S DISCLAIMER

Around 99% of everything contained here I figured out as I went along. This is neither well-planned nor well-executed. The only formal background I have had in coding is an Intro to Programming class I once took Junior year of college. I am not very good at this. 

Should you ever read my code, I apologize in advance. 

_It is not the intent of the author to damage, harm, or otherwise distress any persons, but the author recognizes that written within this repository are things that are potentially damaging, harmful, or distressful to mental health, most especially if the reader should have any expertise in object-oriented programming or mathematics beyond a high-school level._

_<sup>1</sup> Without a Premium or Enterprise account, Twitter provides access only to the last 7 days of Tweets since the current date, while limiting the number of Tweets returned per request. This is decidedly not a good thing if you are starting this project late and cannot afford to drop the [$1900](https://developer.twitter.com/en/docs/tweets/search/overview/premium) on a Premium Developer account to get 1 million tweets  - only 500 Tweets per request adds up._ 

_It is slightly more economical to scrape the front-end (free)._ 

## THE PROCESS

### OVERVIEW
I farmed around 870k Tweets that reference Coachella using [taspinar's](https://github.com/taspinar) [twitterscraper](https://github.com/taspinar/twitterscraper) and sorted through them to find any mentions of musical artists.

Tweets were collected in the time period between 2019-01-03 (when the Coachella line-up was first announced) to four months after, 2019-05-03

I use Python to obtain a weighted adjacency matrix representing how often each artist is co-mentioned with another artist relative to all other co-mentions. 

I then import the adjacency matrix into an R session, create an igraph object from the matrix, and render a visNetwork object from the igraph object.






