from flask import Flask, jsonify
from flask_cors import cross_origin
from CubeModelisation.sentimentCube import SentimentCube
from CubeModelisation.tweetCube import TweetCube

# --------------------------------------------------------------------------------------------------------------------------------------------



def runServer():
    app = Flask(__name__)



    @app.route('/route1', methods=['GET'])
    @cross_origin()
    def sentimentByCountriesAndDatesMapJson():
        sentimentCube = SentimentCube()
        data = sentimentCube.getSentimentByContriesAndDates()
        a = jsonify(data)
        return a

    @app.route('/route2', methods=['GET'])
    @cross_origin()
    def sourcePieChartsByContinentJson():
        tweetCube = TweetCube()
        data = tweetCube.getPieChartSource()
        a = jsonify(data)
        return a

    @app.route('/route3', methods=['GET'])
    @cross_origin()
    def barChartRaceByLanguageAndDateJson():
        tweetCube = TweetCube()
        data = tweetCube.getBarChartRaceByLanguageAndDate()
        a = jsonify(data)
        return a

    app.run(debug=True)


# --------------------------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    # threading.Thread(target=runServer).start()# run local server when starting the app
    runServer()
    # webview.create_window("TWITTER'S CUBE", 'http://127.0.0.1:5000/')
    # webview.start()
