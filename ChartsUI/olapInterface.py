from flask import Flask, jsonify
from flask_cors import cross_origin
from CubeModelisation.sentimentCube import SentimentCube
from CubeModelisation.tweetCube import TweetCube
import pymysql
pymysql.install_as_MySQLdb()
# --------------------------------------------------------------------------------------------------------------------------------------------



def runServer():
    app = Flask(__name__)

    @app.route('/countriesSentiments', methods=['GET'])
    @cross_origin()
    def sentimentByCountriesAndDatesMapJson():
        sentimentCube = SentimentCube()
        data = sentimentCube.getSentimentByCountriesAndDates()
        a = jsonify(data)
        return a

    @app.route('/groupedCountriesSentiments', methods=['GET'])
    @cross_origin()
    def sentimentByCountriesMapJson():
        sentimentCube = SentimentCube()
        data = sentimentCube.getSentimentByCountries()
        a = jsonify(data)
        return a

    @app.route('/tweetsSourcesBycontinent', methods=['GET'])
    @cross_origin()
    def sourcePieChartsByContinentJson():
        tweetCube = TweetCube()
        data = tweetCube.getPieChartSource()
        a = jsonify(data)
        return a

    @app.route('/tweetsByLanguage', methods=['GET'])
    @cross_origin()
    def barChartRaceByLanguageAndDateJson():
        tweetCube = TweetCube()
        data = tweetCube.getBarChartRaceByLanguageAndDate()
        a = jsonify(data)
        return a

    @app.route('/tweetsBySentiments', methods=['GET'])
    @cross_origin()
    def barChartRaceBySentimentAndDateJson():
        tweetCube = TweetCube()
        data = tweetCube.getBarChartRaceBySentimentAndDate()
        a = jsonify(data)
        return a

    app.run(debug=True)


# --------------------------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    # threading.Thread(target=runServer).start()# run local server when starting the app
    runServer()
    # webview.create_window("TWITTER'S CUBE", 'http://127.0.0.1:5000/')
    # webview.start()
