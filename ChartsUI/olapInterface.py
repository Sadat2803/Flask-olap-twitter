from flask import Flask, jsonify
from flask_cors import cross_origin
from CubeModelisation.sentimentCube import SentimentCube

# --------------------------------------------------------------------------------------------------------------------------------------------



def runServer():
    app = Flask(__name__)



    @app.route('/', methods=['GET'])
    @cross_origin()
    def sentimentByCountriesAndDatesMapJson():
        sentimentCube = SentimentCube()
        data = sentimentCube.getSentimentByContriesAndDates()
        return jsonify(data)

    app.run(debug=True)


# --------------------------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    # threading.Thread(target=runServer).start()# run local server when starting the app
    runServer()
    # webview.create_window("TWITTER'S CUBE", 'http://127.0.0.1:5000/')
    # webview.start()
