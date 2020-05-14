from __future__ import print_function

from collections import defaultdict

import cubes
from cubes import Workspace, Cell, PointCut


class SentimentCube:

    def __init__(self, concept):
        self.createCube()
        self.concept = concept

    def createCube(self):
        self.workspace = Workspace()
        self.workspace.register_default_store("sql", url="mysql://root:@localhost/datawarehouse")
        model = cubes.read_model_metadata_bundle("../CubeModelisation/model/")
        self.workspace.import_model(model)
        self.browserTweet = self.workspace.browser("sentiment")


    def getSentimentByCountriesAndDates(self):
        cube = self.workspace.cube("sentiment")
        cube.browser = self.browserTweet

        cut = [PointCut("concept", [self.concept])]
        cell = Cell(cube, cut)

        result = self.browserTweet.aggregate(cell, drilldown=["time:day","location:city"], aggregates=["sentiment_average"])

        output = []
        for row in result.table_rows("location"):
            output.append(row.record)
        data = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
        for row in output:
            if row['location.countryName'] != 'ND':
                date = row['time.year'] + "-" + row['time.month'] + "-" + row['time.day']
                country = row['location.countryName']
                data[date][country]['numberOfNegative'] += 0
                data[date][country]['numberOfPositive'] += 0
                data[date][country]['numberOfNeutral'] += 0
                if row['sentiment_average'] < -0.1:
                    data[date][country]['numberOfNegative'] += 1
                elif row['sentiment_average'] > 0.1:
                    data[date][country]['numberOfPositive'] += 1
                else:
                    data[date][country]['numberOfNeutral'] += 1
        dataList = []
        element = {'date': '', 'countriesList': []}
        import pickle
        with open('../Docs/locations.pickle', 'rb') as file:
            worldCitiesDict = pickle.load(file)
            worldIso2Dict = pickle.load(file)

        for date in data:
            element['date'] = date
            countryElement = {'countryName': '','iso2':'', 'numberOfPositive': 0, 'numberOfNegative': 0, 'numberOfNeutral': 0}
            myCountriesList = []
            for country in data[date]:
                try:
                    countryElement['countryName'] = country
                    countryElement['iso2'] = worldIso2Dict[country]
                    countryElement['numberOfPositive'] = data[date][country]['numberOfPositive']
                    countryElement['numberOfNegative'] = data[date][country]['numberOfNegative']
                    countryElement['numberOfNeutral'] = data[date][country]['numberOfNeutral']
                    myCountriesList.append(countryElement)
                    countryElement = {'countryName': '', 'numberOfPositive': 0, 'numberOfNegative': 0,
                                      'numberOfNeutral': 0}
                except KeyError as e:
                    print("No iso2 available for: "+str(e))
            element['countriesList'] = myCountriesList
            dataList.append(element)
            element = {'date': '', 'countriesList': []}
        return dataList

    def getSentimentByCountries(self):
        cube = self.workspace.cube("sentiment")
        cube.browser = self.browserTweet

        cut = [PointCut("concept", [self.concept])]
        cell = Cell(cube, cut)

        result = self.browserTweet.aggregate(cell, drilldown=["time:day","location:city"], aggregates=["sentiment_average"])
        output = []
        for row in result.table_rows("location"):
            output.append(row.record)
        data = defaultdict(lambda: defaultdict(int))
        for row in output:
            if row['location.countryName'] != 'ND':
                date = row['time.year'] + "-" + row['time.month'] + "-" + row['time.day']
                country = row['location.countryName']
                data[country]['numberOfNegative'] += 0
                data[country]['numberOfPositive'] += 0
                data[country]['numberOfNeutral'] += 0
                if row['sentiment_average'] < -0.1:
                    data[country]['numberOfNegative'] += 1
                elif row['sentiment_average'] > 0.1:
                    data[country]['numberOfPositive'] += 1
                else:
                    data[country]['numberOfNeutral'] += 1
        import pickle
        with open('../Docs/locations.pickle', 'rb') as file:
            worldCitiesDict = pickle.load(file)
            worldIso2Dict = pickle.load(file)

        countryElement = {'countryName': '','iso2':'', 'numberOfPositive': 0, 'numberOfNegative': 0, 'numberOfNeutral': 0}
        myCountriesList = []
        for country in data:
            try:
                countryElement['countryName'] = country
                countryElement['iso2'] = worldIso2Dict[country]
                countryElement['numberOfPositive'] = data[country]['numberOfPositive']
                countryElement['numberOfNegative'] = data[country]['numberOfNegative']
                countryElement['numberOfNeutral'] = data[country]['numberOfNeutral']
                myCountriesList.append(countryElement)
                countryElement = {'countryName': '', 'numberOfPositive': 0, 'numberOfNegative': 0,
                                  'numberOfNeutral': 0}
            except KeyError as e:
                print("No iso2 available for: "+str(e))
        return myCountriesList
