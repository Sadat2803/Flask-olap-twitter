from DWFiles.importsForDB import *

class FactCovCase(Model):
    __fillable__ = ['locationID', 'timeID', 'nbrOfCases', 'nbrOfDeath', 'nbrOfRecovered']
    __timestamps__ = False
    __table__ = "factcovcase"

    def insert(self,row):
        #foreign keys
        self.locationID = row[0]
        self.timeID = row[1]
        # mesures
        self.nbrOfCases = row[2]
        self.nbrOfDeath = row[3]
        self.nbrOfRecovered = row[4]
        self.save()
