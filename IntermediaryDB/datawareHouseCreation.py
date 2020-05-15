from eloquent import DatabaseManager, Model
from DWFiles.dimLanguage import DimLanguage
from DWFiles.dimLocation import DimLocation
from DWFiles.dimSentiment import DimSentiment
from DWFiles.dimSource import DimSource
from DWFiles.dimTime import DimTime
from DWFiles.factCovCase import FactCovCase
from DWFiles.factSentiment import FactSentiment
from DWFiles.factTweet import FactTweet
from DWFiles.dimConcept import DimConcept
import mysql.connector

config = {
        'mysql':{
            'driver': 'mysql',
            'host': 'localhost',
            'database': 'InterDB',
            'user': 'root',
            'password': '',
            'prefix':''
        }
    }

dbIntermediary = DatabaseManager(config)


class DatawareHouseCreation:

    def createDatawareHouse(self, analysisID):

        # get all the different concepts for this client
        allConcepts = dbIntermediary.table('alltweets').select(dbIntermediary.raw('distinct concept')).where('analysisID', '=', analysisID).get()
        configdb = {
            'mysql': {
                'driver': 'mysql',
                'host': 'localhost',
                'database': 'datawarehouse',
                'user': 'root',
                'password': '',
                'prefix': ''
            }
        }

        db = DatabaseManager(configdb)
        Model.set_connection_resolver(db)
        for temp in allConcepts:
            concept = temp['concept']
            print('concept is : ',concept)
            #-----------------------------------------
            # Fill the Fact Tweet Table
            data = dbIntermediary.table('alltweets').select(dbIntermediary.raw('*,count(*) as numberOfTweets'))\
                .where('analysisID', '=', analysisID).where('concept', '=', concept).group_by(
                'languageName', 'sourceName', 'timeAltID', 'sentimentLabel', 'cityName').get()

            conceptTable = DimConcept()
            rowConcept = [concept]
            conceptID = conceptTable.insert(rowConcept)
            cpt = 0
            for row in data:
                rowSentiment = [row['sentimentLabel']]
                rowSource = [row['sourceName']]
                rowTime = [row['timeAltID'], row['dayOfWeek'], row['day'], row['month'], row['monthName'], row['year'],
                           row['season']]
                rowLocation = [row['locationAltID'], row['cityName'], row['countryID'], row['countryName'],
                               row['continentID'], row['continentName']]
                rowLanguage = [row['languageCode'], row['languageName']]

                # instanciate the DB tables
                time = DimTime()
                sentiment = DimSentiment()
                language = DimLanguage()
                location = DimLocation()
                source = DimSource()
                factTweet = FactTweet()

                # fill the dimensions
                timeID = time.insert(rowTime)
                sentimentID = sentiment.insert(rowSentiment)
                languageID = language.insert(rowLanguage)
                locationID = location.insert(rowLocation)
                sourceID = source.insert(rowSource)

                # fill the fact table with foreign keys & mesures
                numberOfTweets = row['numberOfTweets']
                row = [conceptID, locationID, sourceID, languageID, timeID, sentimentID, numberOfTweets]
                factTweet.insert(row)
                cpt += 1
                print(cpt, "tuple inserted", sep=" ")
            print("All tuples are inserted For the Fact Tweet for the concept :", concept)
# ----------------------------------------------------------------------------------------------------------------
            # Fill the Fact Sentiment Table
            data = dbIntermediary.table('alltweets').select(
                dbIntermediary.raw('*,avg(sentimentValue) as averageSentiment'))\
                .where('analysisID', '=', analysisID).where('concept', '=', concept).group_by(
                'languageName', 'timeAltID', 'cityName').get()
            cpt = 0
            for row in data:
                rowTime = [row['timeAltID'], row['dayOfWeek'], row['day'], row['month'], row['monthName'], row['year'],
                           row['season']]
                rowLocation = [row['locationAltID'], row['cityName'], row['countryID'], row['countryName'],
                               row['continentID'], row['continentName']]
                rowLanguage = [row['languageCode'], row['languageName']]

                # instanciate the DB tables
                time = DimTime()
                language = DimLanguage()
                location = DimLocation()
                factSentiment = FactSentiment()

                # fill the dimensions
                timeID = time.insert(rowTime)
                languageID = language.insert(rowLanguage)
                locationID = location.insert(rowLocation)

                # fill the fact table with foreign keys & mesures
                averageSentiment = row['averageSentiment']
                row = [conceptID, locationID, languageID, timeID, averageSentiment]

                factSentiment.insert(row)
                cpt += 1
                print(cpt, "tuple inserted", sep=" ")
            print("All tuples are inserted For the Fact Sentiment for the concept :", concept)
# ----------------------------------------------------------------------------------------------------------------
        # Fill the Fact CovCase Table
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="interDB"
        )
        mycursor = mydb.cursor()
        mycursor.execute("select * from covidstats, alltweets "
                         "where alltweets.timeAltID = covidstats.dateCode and alltweets.countryName = covidstats.country "
                         "group by covidstats.country ,covidstats.date")

        data = mycursor.fetchall()

        cpt = 0
        for row in data:
            rowTime = [row[15], row[16], row[17], row[18], row[19], row[20],
                       row[21]]
            rowLocation = [row[9], row[10], row[11], row[12],
                           row[13], row[14]]

            # instanciate the DB tables
            time = DimTime()
            location = DimLocation()
            factCovCase = FactCovCase()

            # fill the dimensions
            timeID = time.insert(rowTime)
            locationID = location.insert(rowLocation)

            # fill the fact table with foreign keys & mesures
            nbrOfCases = row[3]
            nbrOfDeath = row[4]
            nbrOfRecovered = row[5]
            row = [locationID, timeID, nbrOfCases, nbrOfDeath, nbrOfRecovered]

            factCovCase.insert(row)

            cpt += 1
            print(cpt, "tuple inserted", sep=" ")
        print("All tuples are inserted For the Fact CovCase")


if __name__ == "__main__":
    test = DatawareHouseCreation()
    test.createDatawareHouse()