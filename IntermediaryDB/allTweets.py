from eloquent import DatabaseManager, Model
config = {
            'mysql': {
                'driver': 'mysql',
                'host': 'localhost',
                'database': 'interdb',
                'user': 'root',
                'password': '',
                'prefix': ''
            }
        }
db = DatabaseManager(config)
Model.set_connection_resolver(db)

class AllTweets(Model):

    __fillable__ = ['*']
    __timestamps__ = False
    __primary_key__ = 'tweetID'
    __table__ = 'alltweets'

    def insert(self, row):
        found = AllTweets.where('tweetID', '=', row[0]).where('analysisID', '=', row[20]).where('concept', '=', row[21]).count()
        #found = AllTweets.find(row[0])
        if  found == 0 :
            self.tweetID = row[0]
            self.text = row[1]
            self.languageCode = row[2]
            self.languageName = row[3]

            self.locationAltID = row[4]
            self.cityName = row[5]
            self.countryID = row[6]
            self.countryName = row[7]
            self.continentID = row[8]
            self.continentName = row[9]

            self.timeAltID = row[10]
            self.dayOfWeek = row[11]
            self.day = row[12]
            self.month = row[13]
            self.monthName = row[14]
            self.year = row[15]
            self.season = row[16]

            self.sentimentValue = row[17]
            self.sentimentLabel = row[18]

            self.sourceName = row[19]

            self.analysisID = row[20]
            self.concept = row[21]

            self.save()
        else:
            print("Tweet already exist")




