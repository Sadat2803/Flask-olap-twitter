from DWFiles.importsForDB import *

class DimTime(Model):
    __fillable__ = ['timeAltID','dayOfWeek','day','month','monthName','year','season']
    __timestamps__ = False
    __primary_key__ = 'timeID'
    __table__ = "dimtime"


    def insert(self,row):
        found = DimTime.where('timeAltID', '=', row[0])
        if found.count() == 0:
            self.timeAltID = row[0]
            self.dayOfWeek = row[1]
            self.day = row[2]
            self.month = row[3]
            self.monthName = row[4]
            self.year = row[5]
            self.season = row[6]
            self.save()
            # return the primary key
            return self.timeID
        else:
            #print("Time already exist")
            return found.take(1).get()[0].timeID
