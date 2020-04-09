from DWFiles.importsForDB import *

class DimSentiment(Model):
    __fillable__ = ['sentimentLabel']
    __timestamps__ = False
    __primary_key__ = 'sentimentID'
    __table__ = "dimsentiment"

    def insert(self,row):
        found = DimSentiment.where('sentimentLabel', '=', row[0])
        if found.count() == 0:
            self.sentimentLabel = row[0]
            self.save()
            # return the primary key
            return self.sentimentID
        else:
            #print("sentiment already exist")
            return found.take(1).get()[0].sentimentID

