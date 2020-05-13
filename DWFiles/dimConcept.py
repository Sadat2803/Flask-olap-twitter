from DWFiles.importsForDB import *

class DimConcept(Model):
    __fillable__ = ['conceptLabel']
    __timestamps__ = False
    __primary_key__ = 'conceptID'
    __table__ = "dimconcept"

    def insert(self,row):
        found = DimConcept.where('conceptLabel', '=', row[0])
        if found.count() == 0:
            self.conceptLabel = row[0]
            self.save()
            # return the primary key
            return self.conceptID
        else:
            #print("concept already exist")
            return found.take(1).get()[0].conceptID

