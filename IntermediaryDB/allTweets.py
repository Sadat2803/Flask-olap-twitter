from eloquent import DatabaseManager, Model

config = {
        'mysql':{
            'driver': 'mysql',
            'host': 'localhost',
            'database': 'IntermediaryDB',
            'user': 'root',
            'password': '',
            'prefix':''
        }
    }

db = DatabaseManager(config)
Model.set_connection_resolver(db)

class AllTweets(Model):
    __fillable__ = ['*']
    __timestamps__ = False
    __primary_key__ = 'tweetID'
    __table__ = "alltweets"

    def insert(self, row):
        found = AllTweets.find(row[0])
        if not found:
            self.tweetID = row[0]
            self.languageCode = row[1]
            self.languageName = row[2]

            self.locationAltID = row[3]
            self.cityName = row[4]
            self.countryID = row[5]
            self.countryName = row[6]
            self.continentID = row[7]
            self.continentName = row[8]

            self.timeAltID = row[9]
            self.dayOfWeek = row[10]
            self.day = row[11]
            self.month = row[12]
            self.monthName = row[13]
            self.year = row[14]
            self.season = row[15]

            self.sentimentValue = row[16]
            self.sentimentLabel = row[17]

            self.sourceName = row[18]

            self.save()
        else:
            print("Tweet already exist")




