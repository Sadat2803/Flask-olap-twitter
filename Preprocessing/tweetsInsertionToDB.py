import json
from os import listdir
from os import rename
from os.path import isfile, join
from DBFiles.dimProfile import *
from DBFiles.dimLanguage import *
from DBFiles.dimLocation import *
from DBFiles.dimSentiment import *
from DBFiles.dimTime import *
from DBFiles.dimSource import *
from DBFiles.factTweet import *

from Preprocessing.tweetsPreProcessing import *


class TweetsInsertionToDB():


    def lanchInsertionToDB(self,enrichment):

        preProcessing = TweetsPreProcessing()
        if enrichment == False: #default case
            dirPath = "../TweetFiles/"
        else: #enrichment case
            dirPath = "../EnrichmentFiles/"
        allFiles = [f for f in listdir(dirPath) if isfile(join(dirPath, f))]
        print(allFiles)
        for fileName in allFiles:
            if fileName.startswith("ExtractedTweetsFor"):
                if not fileName.endswith("Loaded.json"): #check if the file is loaded to the database or not
                    fullFileName = dirPath+fileName
                    newFileName = dirPath + fileName.split('.')[0]
                    if not fileName.__contains__("Done"): # add ] } to the file and rename it
                        newFileName +="Done"+'.'+'json'
                        rename(fullFileName, newFileName)
                        tweetsFile = open(newFileName, 'a',encoding="utf-8")
                        tweetsFile.write("\n]\n}")
                        tweetsFile.close()
                    else:
                        newFileName+= "." + "json"
                    tweetsFile = open(newFileName, 'r', encoding="utf-8")
                    tweets = json.load(tweetsFile)
                    cpt=0
                    for tweet in tweets['tweets'][0:1]:
                        time = DimTime()
                        sentiment = DimSentiment()
                        language = DimLanguage()
                        profile = DimProfile()
                        location = DimLocation()
                        source = DimSource()
                        factTweet = FactTweet()

                        #fill the dimensions
                        timeID = time.insert(preProcessing.getTime(tweet['created_at']))
                        sentimentID = sentiment.insert(preProcessing.getSentimentAnalysis(tweet['text']))
                        languageID = language.insert(preProcessing.getLangage(tweet['lang']))
                        profileID = profile.insert(preProcessing.getProfile(tweet['user']))
                        locationID = location.insert(preProcessing.getLocation(tweet['user']['location']))
                        sourceID = source.insert(preProcessing.getSource(tweet['source']))

                        #fill the fact table with foreign keys & mesures
                        favoriteCount = tweet['favorite_count']
                        tweetAltID = tweet['id_str']
                        tweetText = "Text"
                        #tweetText = tweet['text']
                        #tweetText = tweetText.encode('utf-8')
                        row = [tweetAltID, profileID, locationID, sourceID, languageID, timeID, sentimentID, tweetText, favoriteCount]

                        factTweet.insert(row)

                        cpt+=1
                        print(cpt,"tweet inserted",sep=" ")
                    print("For the file : ",fileName,", Tweets number is : ",cpt)
                    tweetsFile.close()
                    # change the name of the file to indicate that this file is loaded into the database
                    if  fileName.__contains__("Done"):
                       newFileName2 = dirPath+fileName.split('.')[0]+"Loaded"+"."+"json"
                    else:
                        newFileName2 = dirPath + fileName.split('.')[0] + "Done" + "Loaded" + "." + "json"
                    rename(newFileName,newFileName2)
            break

        print("All Files are loaded to the database")


if __name__=="__main__":
    test = TweetsInsertionToDB()
    test.lanchInsertionToDB(enrichment=False)