import datetime
import time
import re
from facepy import GraphAPI
import tweepy
import project_credentials
from database_stuff import storeStatement, db

""" Facebook stuff """
fb = GraphAPI(
    project_credentials.fb_token
)

def storeFbPostsFrom(posts, username, leaning):
    """ Saves in DB Facebook posts from a given user, next to its political leaning """
    if leaning not in ["left", "right"]:
        raise Exception("Not a valid political leaning")
    if not type(posts) is list:
        raise Exception("A lists of posts is required")
    if not username:
        username = "unidentified username"

    for statement in posts:
        storeStatement(statement, leaning, username)


def getFbPostsFrom(username, since=(2015, 6, 1)):
    """ Creates a list if FB posts for a given user """
    since_date = datetime.date(*since)
    since_unix_time = time.mktime(since_date.timetuple())

    result_pages = fb.get(
        "{}/posts".format(username),
        page = True,
        since = since_unix_time
    )
    print(result_pages.next())
    posts = []
    for page in result_pages:
        for post in page["data"]:
            if "message" in post:
                statement = removeUrls(post["message"])
                if isRelevantStatement(statement):
                    print(statement.encode("utf-8"))
                    posts.append(statement)
    return posts



def searchFbPostsByHashtag(hashtag, leaning, since=(2015, 6, 1)):
    """ It appears searching posts is deprecated, we may have to give up on this one """
    if leaning not in ["left", "right"]:
        raise Exception("Not a valid political leaning")

    since_date = datetime.date(*since)
    since_unix_time = time.mktime(since_date.timetuple())

    result_pages = fb.search(
        hashtag,
        "post",
        page = True,
        since = since_unix_time
    )

    for page in result_pages:
        for post in page["data"]:
            if "message" in post:
                statement = removeUrls(post["message"])
                if isRelevantStatement(statement):
                    print(statement.encode("utf-8"))
                    storeStatement(statement, leaning, "Default_author")



""" Twitter stuff """
auth = tweepy.OAuthHandler(
    project_credentials.twitter_consumer_key,
    project_credentials.twitter_consumer_secret
)

auth.set_access_token(
    project_credentials.twitter_access_token,
    project_credentials.twitter_access_token_secret
)

api = tweepy.API(auth)

def getTweetsFromHashtag(hashtag, leaning, since=(2015, 6, 1)):
    """ Searches tweets by hashtag, and stores them in DB, next to its political leaning """
    if leaning not in ["left", "right"]:
        raise Exception("Not a valid political leaning")

    for tweet in limitHandled(tweepy.Cursor(api.search, q=hashtag).items()):
        if tweet.created_at < datetime.datetime(*since): break #If we reached the "since" date, just break
        if isRetweet(tweet): tweet.text = tweet.retweeted_status.text #If it's a retweet, access the original tweet
        tweet.text = removeUrls(tweet.text) #URLs shouldn't influence the classification decision
        #If the tweets are too short, or already in DB, disregard them
        if not isRelevantStatement(tweet.text) or isAlreadyInDb(tweet.text): continue
        print(tweet.created_at)
        print(tweet.text.encode("utf-8"))
        #Otherwise, store the tweet in DB
        storeStatement(tweet.text, leaning, "Default_author")


def getTweetsFrom(username, leaning, since=(2015, 6,1)):
    """ Gets a given user's tweets, and stores them in DB, next to its political leaning """
    if leaning not in ["left", "right"]:
        raise Exception("Not a valid political leaning")

    for tweet in limitHandled(tweepy.Cursor(api.user_timeline, id=username).items()):
        if tweet.created_at < datetime.datetime(*since): break
        tweet.text = removeUrls(tweet.text)
        if not isRelevantStatement(tweet.text): continue
        print(tweet.created_at)
        print(tweet.text.encode("utf-8"))
        storeStatement(tweet.text, leaning, username)


def limitHandled(cursor):
    """ Wraps a tweepy cursor with an iterator that handles rate limits """
    while True:
        try:
            yield cursor.next()
        except tweepy.TweepError:
            print("Waiting for Twitter's time limit to expire...")
            time.sleep(20 * 60)




""" Useful extra stuff """

def removeUrls(statement):
    """Takes a string input, and removes the urls in it"""
    urls = re.findall("http[s]?://[^ ]+", statement)
    if urls:
        for url in urls:
            statement = statement.replace(url, "")
    return statement


def isRelevantStatement(statement, min_len = 60):
    return len(statement) > min_len

def isRetweet(tweet):
    if hasattr(tweet, "retweet_status"):
        return True

def isAlreadyInDb(statement):
    c = db.execute("SELECT * FROM statements WHERE statement = ?", (statement, ))
    if c.fetchone():
        return True
