from __future__ import print_function

from collections import defaultdict

import cubes
from cubes import Workspace, Cell, PointCut


class SentimentCube:

    def __init__(self):
        self.createCube()

    def createCube(self):
        self.workspace = Workspace()
        self.workspace.register_default_store("sql",
                                         url="mysql://root:@localhost/tweetsdatawarehouse")

        model = cubes.read_model_metadata_bundle("../CubeModelisation/model/")

        self.workspace.import_model(model)
        self.browserTweet = self.workspace.browser("sentiment")


    def getSentimentByContriesAndDates(self):
        cube = self.workspace.cube("sentiment")
        cube.browser = self.browserTweet
        cell = Cell(cube)

        result = self.browserTweet.aggregate(cell, drilldown=["time:day","location:city"], aggregates=["sentiment_average"])

        output = []
        for row in result.table_rows("location"):
            output.append(row.record)

        data = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
        for row in output:
            date = row['time.year'] + "-" + row['time.month'] + "-" + row['time.month']
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
        for date in data:
            element['date'] = date
            countryElement = {'countryName': '', 'numberOfPositive': 0, 'numberOfNegative': 0, 'numberOfNeutral': 0}
            myCountriesList = []
            for country in data[date]:
                countryElement['countryName'] = country
                countryElement['numberOfPositive'] = data[date][country]['numberOfPositive']
                countryElement['numberOfNegative'] = data[date][country]['numberOfNegative']
                countryElement['numberOfNeutral'] = data[date][country]['numberOfNeutral']
                myCountriesList.append(countryElement)
                countryElement = {'countryName': '', 'numberOfPositive': 0, 'numberOfNegative': 0, 'numberOfNeutral': 0}
            element['countriesList'] = myCountriesList
            dataList.append(element)
            element = {'date': '', 'countriesList': []}
        return dataList
