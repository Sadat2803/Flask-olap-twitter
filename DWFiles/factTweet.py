from DWFiles.importsForDB import *

class FactTweet(Model):
    __fillable__ = ['locationID','sourceID','languageID','timeID','sentimentID','numberOfTweets']
    __timestamps__ = False
    __table__ = "facttweet"
    def insert(self, row):
        #foreign keys
        self.conceptID = row[0]
        self.locationID = row[1]
        self.sourceID = row[2]
        self.languageID = row[3]
        self.timeID = row[4]
        self.sentimentID = row[5]
        #mesures
        self.numberOfTweets = row[6]
        self.save()
