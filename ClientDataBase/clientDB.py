import json
from collections import defaultdict
from datetime import date

import mysql.connector
import pycountry_convert
import pandas as pd
from eloquent import DatabaseManager, Model

from DWFiles.dimLocation import DimLocation
from DWFiles.dimTime import DimTime
from DWFiles.factCovCase import FactCovCase
from IntermediaryDB.covidStats import CovidStats
from Preprocessing.tweetsPreProcessing import TweetsPreProcessing


class ClientDB:

    def createClientDB(self):
        covidFile = open('covid_world_timeline.json', 'r', encoding="utf-8")
        data = json.load(covidFile)

        for row in data:
            date = row['date']
            dateCode = "".join(date.split("-"))
            listCountries = row['list']
            for temp in listCountries:
                countryCode = temp['id'].split('-')[0]
                try:
                    country = pycountry_convert.country_alpha2_to_country_name(countryCode)
                except:
                    country = 'Unknown'
                    if countryCode == 'XK':
                        country = 'Kosovo'
                confirmed = temp['confirmed']
                deaths = temp['deaths']
                recovered = temp['recovered']
                row = [country.lower(), countryCode, date, dateCode, confirmed, deaths, recovered]
                print(row)
                covidStats = CovidStats()
                covidStats.insert(row)
        print("insertion complete")

    def createDatawarehouseClient(self):
        monthList = {
            '01':'Jan',
            '02':'Feb',
            '03':'Mar',
            '04':'Apr',
            '05':'May',
            '06':'Jun',
            '07':'Jul',
            '08':'Aug',
            '09':'Sep',
            '10':'Oct',
            '11':'Nov',
            '12':'Dec'}
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="interDB"
        )
        mycursor = mydb.cursor()
        mycursor.execute("select country, countryCode, date, dateCode, sum(confirmed) as coronaConfirmed,"
                         " sum(deaths) as coronaDeaths, sum(recovered) as coronaRecovered from covidstats "
                         "group by country, countryCode, date, dateCode")
        result = mycursor.fetchall()
        preProcessing = TweetsPreProcessing()
        configdb = {
            'mysql': {
                'driver': 'mysql',
                'host': 'localhost',
                'database': 'clientdb',
                'user': 'root',
                'password': '',
                'prefix': ''
            }
        }

        db = DatabaseManager(configdb)
        Model.set_connection_resolver(db)
        cpt = 0
        for row in result:
            year = row[3][:4]
            month = row[3][4:6]
            day = row[3][6:8]
            dayOfYear = date.fromisoformat(year + '-' + month + '-' + day).timetuple().tm_yday
            spring = range(80, 172)
            summer = range(172, 264)
            autumn = range(264, 355)
            if dayOfYear in spring:
                season = 'spring'
            elif dayOfYear in summer:
                season = 'summer'
            elif dayOfYear in autumn:
                season = 'autumn'
            else:
                season = 'winter'
            timeAltID = row[3]
            monthName = monthList[month]

            rowLocation = preProcessing.getLocation(row[0])
            rowTime = [timeAltID, dayOfYear, day, month, monthName, year, season]

            time = DimTime()
            location = DimLocation()
            factCovCase = FactCovCase()

            # fill the dimensions
            timeID = time.insert(rowTime)
            locationID = location.insert(rowLocation)
            # fill the dimensions

            # fill the fact table with foreign keys & mesures
            nbrOfCases = row[4]
            nbrOfDeath = row[5]
            nbrOfRecovered = row[6]
            row = [locationID, timeID, nbrOfCases, nbrOfDeath, nbrOfRecovered]
            factCovCase.insert(row)
            cpt += 1
            print(cpt)


if __name__=="__main__":
    db = ClientDB()
    #db.createClientDB()
    db.createDatawarehouseClient()