import json
import time
import datetime
from os import path

import tweepy


class TweetsRest():

    def __init__(self, auth):
        self.api = tweepy.API(auth, wait_on_rate_limit=False, wait_on_rate_limit_notify=False)

    def extractTweets(self,tagsList, filePath, dateBegin, dateEnd):
        #,since="2020-03-19" , until="2020-03-20"
        allTweets = tweepy.Cursor(self.api.search, q=tagsList,since=dateBegin , until=dateEnd,count=100).items()
        fileName = filePath

        tweetsFile = open(fileName, "w")
        tweetsFile.write('{ "tweets" : [')
        cpt = 0
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
                if cpt >10:
                    break
                print('Tweets number : '+str(cpt))
            except tweepy.TweepError:
                # wait time
                print(datetime.datetime.now())
                print('Pause Time ')
                time.sleep(16*60)
                tweet = next(allTweets)
            except StopIteration:
                break

