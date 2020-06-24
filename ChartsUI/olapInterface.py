from collections import defaultdict
from datetime import datetime

import mysql.connector
import re
from flask import Flask, jsonify, request
from flask_cors import cross_origin
from CubeModelisation.sentimentCube import SentimentCube
from CubeModelisation.tweetCube import TweetCube


# --------------------------------------------------------------------------------------------------------------------------------------------
from Preprocessing.mainProgramme import MainProgramme
from Preprocessing.topicExtractionFeaturePivotApproach import TopicExtractionFeaturePivotApproach

def runServer():
    app = Flask(__name__)

    @app.route('/relatedTopics', methods=['GET'])
    @cross_origin()
    def relatedTopics():
        analysisID = request.args['analysisID']
        concept = request.args['concept']
        test = TopicExtractionFeaturePivotApproach()
        #test.featurePivotApproach()

        data = []
        a = jsonify(data)
        return a


    @app.route('/deleteAnalysis', methods=['GET'])
    @cross_origin()
    def deleteAnalysis():
        analysisID = request.args['analysisID']
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="interDB"
        )
        mycursor = mydb.cursor()
        query = "delete from alltweets where analysisID = '" + analysisID + "'"
        mycursor.execute(query)
        mycursor.execute('commit')
        data = []
        a = jsonify(data)
        return a

    @app.route('/covidTotalTimeLine', methods=['GET'])
    @cross_origin()
    def covidTotalTimeLine():
        dateBegin = request.args['dateBegin']
        dateEnd = request.args['dateEnd']
        print(dateBegin)
        print(dateEnd)
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="interDB"
        )
        mycursor = mydb.cursor()
        query = "select date, sum(confirmed), sum(deaths), sum(recovered) from covidstats group by date"
        if dateBegin != "" and dateEnd != "":
            temp = dateBegin.split('/')
            dateBegin = '-'.join([temp[2], temp[1], temp[0]])
            temp = dateEnd.split('/')
            dateEnd = '-'.join([temp[2], temp[1], temp[0]])
            query = "select date, sum(confirmed), sum(deaths), sum(recovered) from covidstats where date>= '" + dateBegin + "' and date <= '" + dateEnd + "' group by date"
        mycursor.execute(query)
        result = mycursor.fetchall()

        dataList = []
        element = {'confirmed': 0, 'deaths': 0, 'recovered':0, 'date': ''}
        for row in result:
            element['date'] = row[0].strftime('%Y-%m-%d')
            element['confirmed'] = row[1]
            element['deaths'] = row[2]
            element['recovered'] = row[3]
            dataList.append(element)
            element = {'confirmed': 0, 'deaths': 0, 'recovered':0, 'date': ''}

        a = jsonify(dataList)
        return a

    @app.route('/covidWorldTimeLine', methods=['GET'])
    @cross_origin()
    def covidWorldTimeLine():
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="interDB"
        )
        mycursor = mydb.cursor()
        query = "select date, countryCode, confirmed, deaths, recovered from covidstats"
        mycursor.execute(query)
        result = mycursor.fetchall()

        temp = defaultdict(lambda: list())
        for row in result:
            temp[row[0]] += [{'confirmed':row[2], 'deaths':row[3], 'recovered':row[4], 'id':row[1]}]
        #print(result)
        dataList = []
        element = {'date': '', 'list': []}
        for date in temp:
            element['date'] = date.strftime('%Y-%m-%d')
            element['list'] = temp[date]
            dataList.append(element)
            element = {'date': '', 'list': []}

        a = jsonify(dataList)
        return a

    @app.route('/mondialSentimentByDatesJson', methods=['GET'])
    @cross_origin()
    def mondialSentimentByDatesJson():
        concept = request.args['concept']
        dateBegin = request.args['dateBegin']
        dateEnd = request.args['dateEnd']
        sentimentCube = SentimentCube(concept)
        data = sentimentCube.getMondialSentimentByDates(dateBegin, dateEnd)
        a = jsonify(data)
        return a


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
        analysisID = dataJson['analysisID']
        conceptsList = dataJson['conceptsList']
        numberOfDays = dataJson['numberOfDays']
        numberOfTweets = dataJson['numberOfTweets'] / numberOfDays

        test = MainProgramme(conceptsList, analysisID)

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

        dataOutput = {'numberOfTweets':0, 'numberOfCountries':0, 'numberOfLanguages':0, 'analysisData':[]}

        mycursor = mydb.cursor()
        query = "select count(*) from alltweets where analysisID = '" + analysisID + "'"
        mycursor.execute(query)
        result = mycursor.fetchall()
        dataOutput['numberOfTweets'] = result[0]

        query = "select count(DISTINCT countryname) from alltweets where analysisID = '" + analysisID + "'"
        mycursor.execute(query)
        result = mycursor.fetchall()
        dataOutput['numberOfCountries'] = result[0]

        query = "select count(DISTINCT languageName) from alltweets where analysisID = '" + analysisID + "'"
        mycursor.execute(query)
        result = mycursor.fetchall()
        dataOutput['numberOfLanguages'] = result[0]

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
        elementsList = []
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
            elementsList.append(element)
        dataOutput['analysisData'] = elementsList
        a = jsonify(dataOutput)
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
            if analysisID != "passif":
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
        numberOfTweets = int(request.args['numberOfTweets'])
        test = MainProgramme([],analysisID)
        test.createCubes(analysisID, numberOfTweets)
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
