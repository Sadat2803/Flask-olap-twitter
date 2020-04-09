from DWFiles.importsForDB import *

class FactTweet(Model):
    __fillable__ = ['locationID','sourceID','languageID','timeID','sentimentID','numberOfTweets']
    __timestamps__ = False
    __table__ = "facttweet"

    def insert(self,row):
        #foreign keys
        self.locationID = row[0]
        self.sourceID = row[1]
        self.languageID = row[2]
        self.timeID = row[3]
        self.sentimentID = row[4]
        #mesures
        self.numberOfTweets = row[5]
        self.save()
