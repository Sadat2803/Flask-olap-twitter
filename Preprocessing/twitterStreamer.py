from tweepy import Stream

from Preprocessing.twitterAuthentification import *
from Preprocessing.twitterListener import *

class TwitterStreamer():

    def __init__(self):
        self.twitterAutenticator = TwitterAuthenticator()

    def streamTweets(self, tweetsFilename, tagsList):
        listener = TwitterListener(tweetsFilename)
        auth = self.twitterAutenticator.authenticateTwitterApp()
        stream = Stream(auth, listener)

        # filter tweets by "tags":
        stream.filter(track=tagsList)