from DWFiles.importsForDB import *

class DimLanguage(Model):
    __fillable__ = ['languageCode','languageName']
    __timestamps__ = False
    __primary_key__ = 'languageID'
    __table__ = "dimlanguage"

    def insert(self, row):
        found = DimLanguage.where('languageCode', '=', row[0])
        if found.count() == 0:
            self.languageCode = row[0]
            self.languageName = row[1]
            self.save()
            #return the primary key
            return self.languageID
        else:
            #print("Language already exist")
            return found.take(1).get()[0].languageID




