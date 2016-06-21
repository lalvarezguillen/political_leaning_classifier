import datetime
import time
import re
from facepy import GraphAPI
import tweepy
import project_credentials
from database_stuff import storeStatement

""" Facebook stuff """
fb = GraphAPI(
    project_credentials.decodeCredentials(project_credentials.fb_token)
)

def getFbPostsFrom(username, leaning, since=(2015, 6, 1)):
    if leaning not in ["left", "right"]:
        raise Exception("Not a valid political leaning")

    since_date = datetime.date(*since)
    since_unix_time = time.mktime(since_date.timetuple())

    result_pages = fb.get(
        "{}/posts".format(username),
        page = True,
        since = since_unix_time
    )

    for page in result_pages:
        for post in page["data"]:
            if "message" in post:
                statement = removeUrls(post["message"])
                if isRelevantStatement(statement):
                    print(statement.encode("utf-8"))
                    storeStatement(statement, leaning, username)
                    
def searchFbPostsByHashtag(hashtag, leaning, since=(2015, 6, 1)):
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
    project_credentials.decodeCredentials(project_credentials.twitter_consumer_key),
    project_credentials.decodeCredentials(project_credentials.twitter_consumer_secret)
)

auth.set_access_token(
    project_credentials.decodeCredentials(project_credentials.twitter_access_token),
    project_credentials.decodeCredentials(project_credentials.twitter_access_token_secret)
)

api = tweepy.API(auth)

def getTweetsFromHashtag(hashtag, leaning, since=(2015, 6, 1)):
    if leaning not in ["left", "right"]:
        raise Exception("Not a valid political leaning")
        
    tweets_generator = tweepy.Cursor(api.search, q=hashtag).items()
    
    while True:
        try:
            tweet = tweets_generator.next()
        except tweepy.TweepError:
            print("Waiting for Twitter's time limit to expire...")
            time.sleep(60*16)
            tweet = tweets_generator.next()
        
        if tweet.created_at < datetime.datetime(*since): break
        tweet.text = removeUrls(tweet.text)
        if not isRelevantStatement(tweet.text): break
        print(tweet.created_at)
        print(tweet.text.encode("utf-8"))
        storeStatement(tweet.text, leaning, "Default_author")
        
 
def getTweetsFrom(username, leaning, since=(2015, 6,1)):
    if leaning not in ["left", "right"]:
        raise Exception("Not a valid political leaning")

    tweets_generator = tweepy.Cursor(api.user_timeline, id=username).items()
    
    while True:
        try:
            tweet = tweets_generator.next()
        except tweepy.TweepError:
            print("Waiting for Twitter's time limit to expire...")
            time.sleep(60*16)
            tweet = tweets_generator.next()
            
        if tweet.created_at < datetime.datetime(*since): break
        tweet.text = removeUrls(tweet.text)
        if not isRelevantStatement(tweet.text): break
        print(tweet.created_at)
        print(tweet.text.encode("utf-8"))
        storeStatement(tweet.text, leaning, username)
        
    



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
