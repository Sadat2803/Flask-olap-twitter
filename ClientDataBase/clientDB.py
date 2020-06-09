import json
import pycountry_convert
import pandas as pd

from IntermediaryDB.covidStats import CovidStats


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

if __name__=="__main__":
    db = ClientDB()
    db.createClientDB()
