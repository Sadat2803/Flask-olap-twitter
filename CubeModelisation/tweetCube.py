from __future__ import print_function

from collections import defaultdict

import cubes
from cubes import Workspace, Cell, PointCut


class TweetCube:

    def __init__(self, concept):
        self.createCube()
        self.concept = concept

    def createCube(self):
        self.workspace = Workspace()
        self.workspace.register_default_store("sql",
                                         url="mysql://root:@localhost/datawarehouse")
        model = cubes.read_model_metadata_bundle("../CubeModelisation/model/")
        self.workspace.import_model(model)
        self.browserTweet = self.workspace.browser("tweet")

    def getPieChartSource(self):
        cube = self.workspace.cube("tweet")
        cube.browser = self.browserTweet

        cut = [PointCut("concept", [self.concept])]
        cell = Cell(cube, cut)

        result = self.browserTweet.aggregate(cell, drilldown=["location","source"],aggregates=["numberOfTweets_sum"])
        output = defaultdict(lambda: defaultdict())

        for row in result.table_rows("location"):
            continent = row.record['location.continentName']
            source = row.record['source.sourceName']
            output[continent][source] = row.record['numberOfTweets_sum']
        temp = {'continentName': '',
                'sources': [{'source': '', 'numberOfTweets': ''}, {'source': '', 'numberOfTweets': ''},
                            {'source': '', 'numberOfTweets': ''}, {'source': '', 'numberOfTweets': ''}]}
        print("output ",output)
        i = 0
        data = []
        for continent in output:
            temp['continentName'] = continent
            temp['sources'][i]['source'] = "iPhone"
            temp['sources'][i]['numberOfTweets'] = output[continent].get('iPhone', 0)
            i += 1
            temp['sources'][i]['source'] = "Android"
            temp['sources'][i]['numberOfTweets'] = output[continent].get('Android', 0)
            i += 1
            temp['sources'][i]['source'] = "Web"
            temp['sources'][i]['numberOfTweets'] = output[continent].get('Web', 0)
            i += 1
            temp['sources'][i]['source'] = "Unknown"
            temp['sources'][i]['numberOfTweets'] = output[continent].get('Unknown', 0)
            i = 0
            data.append(temp)
            temp = {'continentName': '',
                'sources': [{'source': '', 'numberOfTweets': ''}, {'source': '', 'numberOfTweets': ''},
                            {'source': '', 'numberOfTweets': ''}, {'source': '', 'numberOfTweets': ''}]}
        return data

    def getBarChartRaceByLanguageAndDate(self):
        cube = self.workspace.cube("tweet")
        cube.browser = self.browserTweet

        cut = [PointCut("concept", [self.concept])]
        cell = Cell(cube, cut)

        result = self.browserTweet.aggregate(cell, drilldown=["time:day", "language"],
                                             aggregates=["numberOfTweets_sum"])
        output = []
        for row in result.table_rows("time"):
            output.append(row.record)
        data = defaultdict(lambda: defaultdict(lambda: defaultdict()))
        languagesList = []
        for row in output:
            date = row['time.day'] + "/" + row['time.month'] + "/" + row['time.year']
            language = row['language.languageName']
            languagesList.append(language)
            # creating data structure containing all languages
            data[date][language]['numberOfTweets'] = row['numberOfTweets_sum']

        #GET LIST OF LANGUAGES FROM FILE
        import pickle
        with open('../Docs/languagesStructure.pickle', 'rb') as file:
            languagesList = pickle.load(file)
        print(len(languagesList))
        element = {'date': '', 'languagesList': []}
        dataList = []
        for date in data:
            element['date'] = date
            element['languagesList'] = []
            print(len(languagesList))
            for language in languagesList:
                if language in data[date]:
                    element['languagesList'].append({'language':language,'numberOfTweets':data[date][language]['numberOfTweets']})
                else:
                    element['languagesList'].append({'language':language,'numberOfTweets':0})
            dataList.append(element)
        return dataList


    def getBarChartRaceBySentimentAndDate(self):
        cube = self.workspace.cube("tweet")
        cube.browser = self.browserTweet

        cut = [PointCut("concept", [self.concept])]
        cell = Cell(cube, cut)

        result = self.browserTweet.aggregate(cell, drilldown=["time:day", "sentiment"],
                                             aggregates=["numberOfTweets_sum"])

        output = []
        for row in result.table_rows("time"):
            output.append(row.record)

        data = defaultdict(lambda: defaultdict(lambda: defaultdict()))
        for row in output:
            date = row['time.day'] + "/" + row['time.month'] + "/" + row['time.year']
            sentiment = row['sentiment.sentimentLabel']
            data[date][sentiment]['numberOfTweets'] = row['numberOfTweets_sum']
        dataList = []
        element = {'date': '', 'sentimentsList': []}
        for date in data:
            element['date'] = date
            sentimentElement = {'sentiment': '', 'numberOfTweets': 0}
            mySentimentsList = []
            for sentiment in data[date]:
                sentimentElement['sentiment'] = sentiment
                sentimentElement['numberOfTweets'] = data[date][sentiment]['numberOfTweets']
                mySentimentsList.append(sentimentElement)
                sentimentElement = {'sentiment': '', 'numberOfTweets': 0}
            element['sentimentsList'] = mySentimentsList
            dataList.append(element)
            element = {'date': '', 'sentimentsList': []}
        return dataList

