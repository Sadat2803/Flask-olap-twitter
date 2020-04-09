from DWFiles.importsForDB import *

class DimSource(Model):
    __fillable__ = ['sourceName']
    __timestamps__ = False
    __primary_key__ = 'sourceID'
    __table__ = "dimsource"

    def insert(self,row):
        found = DimSource.where('sourceName', '=', row[0])
        if found.count() == 0:
            self.sourceName = row[0]
            self.save()
            # return the primary key
            return self.sourceID
        else:
            #print("source already exist")
            return found.take(1).get()[0].sourceID

