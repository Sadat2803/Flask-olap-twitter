from DWFiles.importsForDB import *

class FactSentiment(Model):
    __fillable__ = ['locationID','languageID','timeID','averageSentiment']
    __timestamps__ = False


    def insert(self,row, sentimentCubeName):
        #foreign keys
        self.__table__ = sentimentCubeName
        self.locationID = row[0]
        self.languageID = row[1]
        self.timeID = row[2]
        # mesures
        self.averageSentiment = row[3]
        self.save()
