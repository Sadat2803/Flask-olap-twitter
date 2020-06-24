import datetime
import os
from time import perf_counter
import mysql

from IntermediaryDB.datawareHouseCreation import DatawareHouseCreation
from IntermediaryDB.tweetsInsersionToIntermediaryDB import TweetsInsertionIntermediaryToDB
from Preprocessing.tweetExtraction2 import TweetsRest
from Preprocessing.twitterAuthentification import TwitterAuthenticator




class MainProgramme():

    def __init__(self, conceptsList, analysisID):
        self.conceptsList = conceptsList
        temp = str(datetime.datetime.today()).split()
        temp[1] = temp[1].replace(":", "-")
        if analysisID =="":
            self.analysisID = "Analysis-" + temp[0] + "_" + temp[1].split('.')[0]
        else:
            self.analysisID = analysisID

    def extractAndSaveDataIntoIntermediaryDB(self, numberOfDays, numberOfTweets):
        # create a folder for this client

        fullPath = "../TweetFilesByClients/" + self.analysisID
        if not os.path.isdir(fullPath):
            os.mkdir(fullPath)
        #print("Directory ", fullPath, " Created ")
        cpt = 0
        # extract data for each concept and save into intermediary BD and then create DW and Cubes
        for concept in self.conceptsList:
            # create a folder for each concept
            cpt += 1
            conceptFolderPath = fullPath+"/"+"Concept-"+str(cpt)
            if not os.path.isdir(conceptFolderPath):
                os.mkdir(conceptFolderPath)
            #print("Directory ", conceptFolderPath, " Created ")
            # extract tweets for this current concept
            twitterAuthentificator = TwitterAuthenticator()
            tweetsRest = TweetsRest(twitterAuthentificator.auth)
            date = datetime.datetime.today()
            #numberOfDays = 2 # from today to 1 day ago
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
                tweetsRest.extractTweets(concept, filePath, dateBegin, dateEnd, numberOfTweets)
        print("tweets extraction done!")


        #insert tweets into the intermediary database
        cpt = 0
        fullPath = "../TweetFilesByClients/" +self.analysisID

        tweetsInsertionIntermediaryToDB = TweetsInsertionIntermediaryToDB()

        for concept in self.conceptsList:
            cpt += 1
            conceptFolderPath = fullPath + "/" + "Concept-" + str(cpt) + "/"
            tweetsInsertionIntermediaryToDB.lanchInsertionToIntermediaryDB(False, conceptFolderPath, concept.lower(), self.analysisID)
        print("tweets insertion into intermediary database done!")
        return self.analysisID

    def createCubes(self, analysisID, numberOfTweets):

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
            mycursor.execute("TRUNCATE " + table)
        mycursor.close()
        print("reinitialisation de la base de donnée")
        #time.sleep(10)
        # create the datawarehouse
        datawareHouseCreation = DatawareHouseCreation()
        datawareHouseCreation.createDatawareHouse(analysisID, numberOfTweets)
        print("datawarehouse crée!")
        #--------------------------------------------

if __name__=="__main__":
    conceptsList = ["StayAtHome", "panicBuying"]
    test = MainProgramme(conceptsList,'passif')
    #test.extractAndSaveDataIntoIntermediaryDB()
    t1_start = perf_counter()
    analysisID = 'passif'
    test.createCubes(analysisID)
    t2_end = perf_counter()
    print(t1_start)
    print(t2_end)
    print(t2_end - t1_start)




