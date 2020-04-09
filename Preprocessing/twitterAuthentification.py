from tweepy import OAuthHandler

from Preprocessing import twitterCredentials
from Preprocessing.tweetsExtraction import TweetsRest


class TwitterAuthenticator():

    def __init__(self):
        self.auth = OAuthHandler(twitterCredentials.consumerKey, twitterCredentials.consumerSecret)
        self.auth.set_access_token(twitterCredentials.accessToken, twitterCredentials.accessTokenSecret)

if __name__ == '__main__':
    tagsList = ['corona','coronavirus','COVID-19','COVID19']
    twitterAuthentificator = TwitterAuthenticator()
    tweetsRest = TweetsRest(twitterAuthentificator.auth)
    # we have to pass 'False' by default
    tweetsRest.extractTweets(tagsList, enrichment=False)



    """
    #TwitterStreamer
    tagsList = ['corona','tsunami']
    tweetsfilename = "myTweets.json"
    twitter_streamer = TwitterStreamer()
    twitter_streamer.streamTweets(tweetsfilename, tagsList)
    """