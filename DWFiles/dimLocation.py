from DWFiles.importsForDB import *

class DimLocation(Model):
    __fillable__ = ['locationAltID','cityName','countryID',
                    'countryName', 'continentID', 'continentName']
    __timestamps__ = False
    __primary_key__ = 'locationID'
    __table__ = "dimlocation"

    def insert(self,row):
        found = DimLocation.where('locationAltID', '=', row[0])
        if found.count() == 0:
            self.locationAltID = row[0]
            self.cityName = row[1]
            self.countryID = row[2]
            self.countryName = row[3]
            self.continentID = row[4]
            self.continentName = row[5]
            self.save()
            # return the primary key
            return self.locationID
        else:
            #print("Location already exist")
            return found.take(1).get()[0].locationID

