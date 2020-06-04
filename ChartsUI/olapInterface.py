from collections import defaultdict

import mysql.connector
import re
from flask import Flask, jsonify, request
from flask_cors import cross_origin
from CubeModelisation.sentimentCube import SentimentCube
from CubeModelisation.tweetCube import TweetCube

# --------------------------------------------------------------------------------------------------------------------------------------------
from Preprocessing.mainProgramme import MainProgramme


def runServer():
    app = Flask(__name__)

    @app.route('/extractConceptsFromClientDW', methods = ['GET'])
    @cross_origin()
    def extractConceptsFromClientDW():
        clientDW = request.args['clientDWPath']
        clientDWPath = '../ClientDW/' + clientDW
        f = open(clientDWPath,'r').read()
        # first, let search for the fact table creation queries
        queries = re.findall("CREATE TABLE IF NOT EXISTS `fact[A-Za-z0-9]+` \(([\n`\(\), \w]+)\)",f)
        temp = []
        for query in queries:
            result = re.findall("`(\w+)`", query)
            temp += result
        conceptList = []
        for word in temp:
            if not (word.lower().startswith('id') or word.lower().endswith('id')):
                conceptList.append(word)
        #print(conceptList)
        a = jsonify(conceptList)
        return a

    @app.route('/launchAnalysis', methods=['POST'])
    @cross_origin()
    def launchAnalysis():
        print(request.json)
        dataJson = request.json
        conceptsList = dataJson['conceptsList']
        numberOfDays = dataJson['numberOfDays']
        numberOfTweets = dataJson['numberOfTweets'] / numberOfDays

        test = MainProgramme(conceptsList)

        analysisID = test.extractAndSaveDataIntoIntermediaryDB(numberOfDays, numberOfTweets)
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="interDB"
        )
        mycursor = mydb.cursor()
        query = "select text, languageName, cityName, countryName, continentName, day, month, year, concept from alltweets where analysisID = '" + analysisID + "'"
        mycursor.execute(query)

        result = mycursor.fetchall()
        element = {
            'text': '',
            'language': '',
            'city': '',
            'country': '',
            'continent': '',
            'date': '',
            'concept': ''
        }
        returnObject = {"analysisID": analysisID, "dataList": []}
        dataList = []
        for row in result:
            element['text'] = row[0]
            element['language'] = row[1]
            element['city'] = row[2]
            element['country'] = row[3]
            element['continent'] = row[4]
            element['date'] = row[5] + "/" + row[6] + "/" + row[7]
            element['concept'] = row[8]
            element = {
                'text': '',
                'language': '',
                'city': '',
                'country': '',
                'continent': '',
                'date': '',
                'concept': ''
            }
            dataList.append(element)

        returnObject["dataList"] = dataList
        a = jsonify(returnObject)
        return a


    @app.route('/getTweets', methods=['GET'])
    @cross_origin()
    def getTweets():
        analysisID = request.args['analysisID']
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="interDB"
        )
        mycursor = mydb.cursor()
        query = "select text, languageName, cityName, countryName, continentName, day, month, year, concept from alltweets where analysisID = '" + analysisID+"'"
        mycursor.execute(query)
        result = mycursor.fetchall()
        element = {
            'text': '',
            'language': '',
            'city': '',
            'country': '',
            'continent': '',
            'date': '',
            'concept': ''
        }
        dataList = []
        for row in result:
            element['text'] = row[0]
            element['language'] = row[1]
            element['city'] = row[2]
            element['country'] = row[3]
            element['continent'] = row[4]
            element['date'] = row[5]+"/"+row[6]+"/"+row[7]
            element['concept'] = row[8]
            element = {
                'text': '',
                'language': '',
                'city': '',
                'country': '',
                'continent': '',
                'date': '',
                'concept': ''
            }
            dataList.append(element)
        a = jsonify(dataList)
        return a


    @app.route('/sentimentByCountriesAndDatesMapJson', methods=['GET'])
    @cross_origin()
    def sentimentByCountriesAndDatesMapJson():
        concept = request.args['concept']
        sentimentCube = SentimentCube(concept)
        data = sentimentCube.getSentimentByCountriesAndDates()
        a = jsonify(data)
        return a

    @app.route('/groupedCountriesSentiments', methods=['GET'])
    @cross_origin()
    def sentimentByCountriesMapJson():
        concept = request.args['concept']
        sentimentCube = SentimentCube(concept)
        data = sentimentCube.getSentimentByCountries()
        a = jsonify(data)
        return a


    @app.route('/tweetsSourcesByContinent', methods=['GET'])
    @cross_origin()
    def sourcePieChartsByContinentJson():
        concept = request.args['concept']
        tweetCube = TweetCube(concept)
        data = tweetCube.getPieChartSource()
        a = jsonify(data)
        return a

    @app.route('/tweetsByLanguage', methods=['GET'])
    @cross_origin()
    def barChartRaceByLanguageAndDateJson():
        concept = request.args['concept']
        tweetCube = TweetCube(concept)
        data = tweetCube.getBarChartRaceByLanguageAndDate()
        a = jsonify(data)
        return a

    @app.route('/tweetsBySentiment', methods=['GET'])
    @cross_origin()
    def barChartRaceBySentimentAndDateJson():
        concept = request.args['concept']
        tweetCube = TweetCube(concept)
        data = tweetCube.getBarChartRaceBySentimentAndDate()
        a = jsonify(data)
        return a

    @app.route('/getConceptsByAnalysis', methods=['GET'])
    @cross_origin()
    def getConceptsByAnalysis():
        #analysisID = request.args['analysisID']
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="interDB"
        )
        mycursor = mydb.cursor()
        mycursor.execute("select analysisID, concept from alltweets "
                         "group by analysisID, concept")
        result = mycursor.fetchall()

        temp = defaultdict(lambda: list())
        for row in result:
            temp[row[0]] += [row[1]]

        dataList = []
        element = {'analysisId': '', 'analysisName': '', 'analysisConcepts': []}

        for analysisID in temp:
            element['analysisId'] = analysisID
            element['analysisName'] = analysisID
            element['analysisConcepts'] = []
            for concept in temp[analysisID]:
                element['analysisConcepts'].append(concept)
            dataList.append(element)
            element = {'analysisId': '', 'analysisName': '', 'analysisConcepts': []}

        a = jsonify(dataList)
        return a

    @app.route('/getConceptsByAnalysisId', methods=['GET'])
    @cross_origin()
    def getConceptsByAnalysisId():
        analysisID = request.args['analysisID']
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="interDB"
        )
        mycursor = mydb.cursor()
        mycursor.execute("select analysisID, concept from alltweets where analysisID = '"+analysisID+"'"
                         "group by analysisID, concept")
        result = mycursor.fetchall()
        element = {'analysisId': analysisID, 'analysisName': analysisID, 'analysisConcepts': []}
        for tuple in result:
            element['analysisConcepts'].append(tuple[1])
        a = jsonify(element)
        return a

    @app.route('/createCubeForAnAnalysis', methods=['GET'])
    @cross_origin()
    def createCubeForAnAnalysis():
        analysisID = request.args['analysisID']
        test = MainProgramme([])
        test.createCubes(analysisID)
        data = []
        a = jsonify(data)
        return a
    app.run(debug=True)


# --------------------------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    # threading.Thread(target=runServer).start()# run local server when starting the app
    runServer()
    # webview.create_window("TWITTER'S CUBE", 'http://127.0.0.1:5000/')
    # webview.start()
