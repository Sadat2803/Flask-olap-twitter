import json
import time
import datetime
from os import path

import tweepy


class TweetsRest():

    def __init__(self, auth):
        self.api = tweepy.API(auth, wait_on_rate_limit=False, wait_on_rate_limit_notify=False)

    def extractTweets(self,tagsList,enrichment):
        #,since="2020-03-19" , until="2020-03-20"
        allTweets = tweepy.Cursor(self.api.search, q=tagsList,since="2020-05-07" , until="2020-05-08",count=100).items()
        if enrichment:
            fileName = "../EnrichmentFiles/ExtractedTweetsFor-" + str(datetime.datetime.today()).split()[0] + ".json"
        else:
            fileName = "../TweetFiles/ExtractedTweetsFor-"+str(datetime.datetime.today()).split()[0]+".json"

        boolAppend = False
        if( path.exists(fileName)):
            tweetsFile = open(fileName, "a")
            boolAppend = True
        else:
            tweetsFile = open(fileName, "w")
            tweetsFile.write('{ "tweets" : [')
        cpt = 0
        if boolAppend==False:
            try:
                tweet = next(allTweets)
                tweetsFile.write(json.dumps(tweet._json, sort_keys="False", indent=4))
                print('Tweets number : ' + str(cpt))
            except tweepy.TweepError:
                # wait time
                print(datetime.datetime.now())
                print('Pause Time ')
                time.sleep(16 * 60)
                tweet = next(allTweets)

        while True:
            try:
                tweet = next(allTweets)
                tweetsFile.write(","+json.dumps(tweet._json, sort_keys="False", indent=4))
                cpt+=1
                print('Tweets number : '+str(cpt))
            except tweepy.TweepError:
                # wait time
                print(datetime.datetime.now())
                print('Pause Time ')
                time.sleep(16*60)
                tweet = next(allTweets)
            except StopIteration:
                break

