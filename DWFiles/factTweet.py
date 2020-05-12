from DWFiles.importsForDB import *

class FactTweet(Model):
    __fillable__ = ['locationID','sourceID','languageID','timeID','sentimentID','numberOfTweets']
    __timestamps__ = False

    def insert(self,row, tweetCubeName):
        #foreign keys
        self.__table__ = tweetCubeName
        self.locationID = row[0]
        self.sourceID = row[1]
        self.languageID = row[2]
        self.timeID = row[3]
        self.sentimentID = row[4]
        #mesures
        self.numberOfTweets = row[5]
        self.save()
