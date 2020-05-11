import datetime
import os
import time

import mysql

from IntermediaryDB.datawareHouseCreation import DatawareHouseCreation
from IntermediaryDB.tweetsInsersionToIntermediaryDB import TweetsInsertionIntermediaryToDB
from Preprocessing.tweetExtraction2 import TweetsRest
from Preprocessing.twitterAuthentification import TwitterAuthenticator




class MainProgramme():

    def __init__(self, conceptsList):
        self.conceptsList = conceptsList
        temp = str(datetime.datetime.today()).split()
        temp[1] = temp[1].replace(":", "-")
        self.clientID = "Client-" + temp[0] + "_" + temp[1].split('.')[0]

    def extractAndSaveDataIntoIntermediaryDB(self):
        # create a folder for this client
        """
        fullPath = "../TweetFilesByClients/" + self.clientID
        os.mkdir(fullPath)
        #print("Directory ", fullPath, " Created ")
        cpt = 0
        # extract data for each concept and save into intermediary BD and then create DW and Cubes
        for concept in self.conceptsList:
            # create a folder for each concept
            cpt += 1
            conceptFolderPath = fullPath+"/"+"Concept-"+str(cpt)
            os.mkdir(conceptFolderPath)
            #print("Directory ", conceptFolderPath, " Created ")
            # extract tweets for this current concept
            twitterAuthentificator = TwitterAuthenticator()
            tweetsRest = TweetsRest(twitterAuthentificator.auth)
            date = datetime.datetime.today()
            numberOfDays = 2 # from today to 1 day ago
            for i in range(numberOfDays):
                tempDate = date
                dateBegin = str(tempDate).split()[0]
                tempDate += datetime.timedelta(days=1)
                dateEnd = str(tempDate).split()[0]
                date -= datetime.timedelta(days=1)
                filePath = conceptFolderPath + "/ExtractedTweetsFor-" + dateBegin+ ".json"
                print(filePath)
                #save keyword into text file "readme.txt"
                f = open(conceptFolderPath + "/readme.txt","w")
                f.write(concept)
                f.close()
                tweetsRest.extractTweets(concept, filePath, dateBegin, dateEnd)
        print("tweets extraction done!")
        """
        #insert tweets into the intermediary database
        cpt = 0
        fullPath = "../TweetFilesByClients/" +"Client-2020-05-05_15-52-41" #self.clientID
        tweetsInsertionIntermediaryToDB = TweetsInsertionIntermediaryToDB()
        for concept in self.conceptsList:
            cpt += 1
            conceptFolderPath = fullPath + "/" + "Concept-" + str(cpt) + "/"
            tweetsInsertionIntermediaryToDB.lanchInsertionToIntermediaryDB(False, conceptFolderPath, concept.lower(), self.clientID)
        print("tweets insertion into intermediary database done!")

    def createCubes(self, clientID):

        #reset the database for owr new analyse
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="datawarehouse"
        )
        mycursor = mydb.cursor()
        mycursor.execute("show tables")
        tablesName = mycursor.fetchall()
        for row in tablesName:
            table = row[0]
            if table.startswith("factsentiment") or table.startswith("facttweet"):
                mycursor.execute("DROP TABLE " + table)
            else:
                mycursor.execute("TRUNCATE " + table)
        mycursor.close()
        print("reinitialisation de la base de donnée")
        #time.sleep(10)
        datawareHouseCreation = DatawareHouseCreation()
        datawareHouseCreation.createDatawareHouse(clientID)
        #--------------------------------------------
        # create the json model
        #first we have to reinisialise the modele
        dirPath = '../CubeModelisation/model/'
        filesList = [f for f in os.listdir(dirPath) if os.path.isfile(os.path.join(dirPath, f))]
        for fileName in filesList:
            if fileName.startswith("cube_tweet_") or fileName.startswith("cube_sentiment_"):
                # delete the file
                path = dirPath+fileName
                os.remove(path)
                print(path, " is deleted")

        tweetCube = open("../CubeModelisation/cube_tweet_example.json", "r").read()
        sentimentcube = open("../CubeModelisation/cube_sentiment_example.json", "r").read()
        for row in tablesName:
            table = row[0]
            if table.startswith("factsentiment"):
                concept = table[13:]
                f = open("../CubeModelisation/model/cube_sentiment_" + concept + ".json","w")
                f.write(sentimentcube.replace("#conceptName#", concept))
                f.close()
            if table.startswith("facttweet"):
                concept = table[9:]
                f = open("../CubeModelisation/model/cube_tweet_" + concept + ".json", "w")
                f.write(tweetCube.replace("#conceptName#", concept))
                f.close()
        print("creation du modèle est faite")






if __name__=="__main__":
    conceptsList = ["StayAtHome", "panicBuying"]
    test = MainProgramme(conceptsList)
    #test.extractAndSaveDataIntoIntermediaryDB()
    clientID = 'Client-2020-05-07_19-26-13'
    test.createCubes(clientID)



