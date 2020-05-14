from DWFiles.importsForDB import *

class FactSentiment(Model):
    __fillable__ = ['locationID','languageID','timeID','averageSentiment']
    __timestamps__ = False
    __table__ = "factsentiment"

    def insert(self, row):
        #foreign keys
        self.conceptID = row[0]
        self.locationID = row[1]
        self.languageID = row[2]
        self.timeID = row[3]
        # mesures
        self.averageSentiment = row[4]
        self.save()
