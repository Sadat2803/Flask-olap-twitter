import json
from nltk import defaultdict
from os import listdir
from os import rename
from os.path import isfile, join
from IntermediaryDB.allTweets import AllTweets
import re
from nltk.corpus import stopwords
from Preprocessing.tweetsPreProcessing import *
import preprocessor as p
class TweetsInsertionIntermediaryToDB():


    def lanchInsertionToIntermediaryDB(self,enrichment, folderPath, concept, analysisID):

        preProcessing = TweetsPreProcessing()
        if enrichment == False: #default case
            dirPath = "../TweetFiles/"
        else: #enrichment case
            dirPath = "../EnrichmentFiles/"
        dirPath = folderPath
        print(dirPath)
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
                    for tweet in tweets['tweets']:
                        allTweets = AllTweets()
                        tweetID = tweet['id_str']
                        text = p.clean(tweet['text'])
                        text = " ".join(re.findall('\w+', text))
                        #text = "text"
                        row = [tweetID, text]
                        row += preProcessing.getLangage(tweet['lang']) + preProcessing.getLocation(tweet['user']['location'])\
                               + preProcessing.getTime(tweet['created_at']) + preProcessing.getSentimentAnalysis(tweet['text'])\
                               + preProcessing.getSource(tweet['source'])
                        row += [analysisID, concept]
                        print(row)
                        allTweets.insert(row)
                        cpt+=1
                        print(cpt,"tweet ",sep=" ")
                    print("For the file : ",fileName,", Tweets number is : ",cpt)
                    tweetsFile.close()
                    # change the name of the file to indicate that this file is loaded into the database
                    if  fileName.__contains__("Done"):
                       newFileName2 = dirPath+fileName.split('.')[0]+"Loaded"+"."+"json"
                    else:
                        newFileName2 = dirPath + fileName.split('.')[0] + "Done" + "Loaded" + "." + "json"
                    rename(newFileName,newFileName2)
        print("All Files are loaded to the intermediary database")

    def renameFiles(self):
        dirPath = "../TweetFiles/"

        allFiles = [f for f in listdir(dirPath) if isfile(join(dirPath, f))]
        print(allFiles)
        for fileName in allFiles:
            if fileName.startswith("ExtractedTweetsFor"):
                newFileName = fileName.replace("Loaded","")
                print(fileName)
                print(newFileName)
                rename(dirPath+fileName, dirPath+newFileName)
        print("Done !")

    def getDistinctTweets(self):
        dirPath = "../TweetFiles/"
        allFiles = [f for f in listdir(dirPath) if isfile(join(dirPath, f))]
        listTweet = set()
        listText = set()
        listUser = set()
        cpt = 0
        for fileName in allFiles:
            if fileName.startswith("ExtractedTweetsFor"):
                tweetsFile = open(dirPath+fileName, 'r', encoding="utf-8")
                tweets = json.load(tweetsFile)

                for tweet in tweets['tweets']:
                    cpt+=1
                    listTweet.add(tweet["id_str"])
                    listText.add(tweet['text'])
                    listUser.add(tweet['user']['id_str'])
        print(cpt)
        print(listTweet.__len__())
        print(listText.__len__())
        print(listUser.__len__())


    def lanchInsertionToDB(self,enrichment):

        if enrichment == False: #default case
            dirPath = "../TweetFiles/"
        else: #enrichment case
            dirPath = "../EnrichmentFiles/"
        allFiles = [f for f in listdir(dirPath) if isfile(join(dirPath, f))]
        print(allFiles)
        cpt = 0
        i = 0
        for fileName in allFiles:
            if fileName.startswith("ExtractedTweetsFor"):
                fullFileName = dirPath + fileName
                tweetsFile = open(fullFileName, 'r', encoding="utf-8")
                tweets = json.load(tweetsFile)

                for tweet in tweets['tweets']:
                    tweetID = tweet['id_str']
                    tweetLanguage = tweet['lang']
                    if tweetLanguage =="en":
                        found = AllTweets.find(tweetID)
                        if found:
                            if found.text == "":
                                tweetText = p.clean(tweet['text'])
                                print(tweetText)
                                #tweetText = tweetText.encode('unicode-escape').decode('utf-8')
                                found.text = tweetText
                                found.save()
                                i += 1
                                print(i," lignes updated")
                    cpt += 1
                    print(cpt,"tweet number")
                tweetsFile.close()


    def treatFiles(self):
        dirPathIn = "../TweetFiles/"
        dirPathOut = "../TweetFiles2/"
        monthList = {
            'Jan': '01',
            'Feb': '02',
            'Mar': '03',
            'Apr': '04',
            'May': '05',
            'Jun': '06',
            'Jul': '07',
            'Aug': '08',
            'Sep': '09',
            'Oct': '10',
            'Nov': '11',
            'Dec': '12'}
        allFiles = [f for f in listdir(dirPathIn) if isfile(join(dirPathIn, f))]
        #print(allFiles)
        for fileName in allFiles:
            if fileName.startswith("ExtractedTweetsFor"):
                newFileName = fileName.replace("Done", "")
                tweetsFileIn = open(dirPathIn+fileName, 'r', encoding="utf-8")
                tweets = json.load(tweetsFileIn)

                tweetsFileOut = open(dirPathOut+newFileName, "w")
                tweetsFileOut.write('{ "tweets" : [')
                cpt = 0
                fileDate = fileName[19:-9]
                firstTweet = False
                tweetsIdList = []
                for tweet in tweets['tweets']:
                    tweetID = tweet['id_str']
                    fullCreationDate = tweet['created_at']
                    day = fullCreationDate[8:10]
                    month = monthList[fullCreationDate[4:7]]
                    year = fullCreationDate[26:31]
                    tweetsDate = year+'-'+month+'-'+day
                    if tweetsDate == fileDate:
                        if firstTweet == False:
                            tweetsFileOut.write(json.dumps(tweet, sort_keys="False", indent=4))
                            tweetsIdList.append(tweetID)
                            firstTweet = True
                        else:
                            if tweetID not in tweetsIdList:
                                tweetsFileOut.write(","+json.dumps(tweet, sort_keys="False", indent=4))
                                tweetsIdList.append(tweetID)
                                cpt += 1
                tweetsFileOut.write("\n]\n}")
                tweetsFileOut.close()
                cpt += 1
                print(fileName, "done!, it contains : ",cpt,' tweets')
                cpt = 0
                tweetsIdList = []

        print("All files done !")
        
        
    def getKeyWordsFromTweets(self):
        result = AllTweets.where("languageCode","=","en").where("text","!=","").get()
        wordFrequency = defaultdict(int)
        stopWords = set(stopwords.words('english'))

        for row in result:
            text = row.text.lower()
            tokens = re.findall("[a-zA-Z]{2,}",text)
            for token in tokens:
                if token not in stopWords:
                    wordFrequency[token]+=1
        w = sorted(wordFrequency.items(), key=lambda wordFrequency: wordFrequency[1], reverse=True)
        print(w)


    def lanchInsertionToIntermediaryDB2(self):
        concept = "coronavirus"
        analysisID = "passif"

        preProcessing = TweetsPreProcessing()
        dirPath = "../TweetFiles/"
        allFiles = [f for f in listdir(dirPath) if isfile(join(dirPath, f))]
        print(allFiles)
        for fileName in allFiles:
            if fileName.startswith("ExtractedTweetsFor"):
                if not fileName.endswith("Loaded.json"): #check if the file is loaded to the database or not
                    fullFileName = dirPath+fileName
                    tweetsFile = open(fullFileName, 'r', encoding="utf-8")
                    tweets = json.load(tweetsFile)
                    cpt=0
                    for tweet in tweets['tweets']:
                        allTweets = AllTweets()

                        tweetID = tweet['id_str']
                        text = p.clean(tweet['text'])
                        text = " ".join(re.findall('\w+', text))
                        #text = "text"
                        row = [tweetID, text]
                        row += preProcessing.getLangage(tweet['lang']) + preProcessing.getLocation(tweet['user']['location'])\
                               + preProcessing.getTime(tweet['created_at']) + preProcessing.getSentimentAnalysis(tweet['text'])\
                               + preProcessing.getSource(tweet['source'])
                        row += [analysisID, concept]
                        print(row)
                        allTweets.insert(row)
                        cpt+=1
                        print(cpt,"tweets ",sep=" ")
                    print("For the file : ",fileName,", Tweets number is : ",cpt)
                    tweetsFile.close()
                    # change the name of the file to indicate that this file is loaded into the database
                    newFileName = dirPath+fileName.split('.')[0]+"Loaded"+"."+"json"
                    rename(fullFileName, newFileName)


        print("All Files are loaded to the intermediary database")



if __name__=="__main__":
    test = TweetsInsertionIntermediaryToDB()
    #test.lanchInsertionToIntermediaryDB(enrichment=False)
    #test.lanchInsertionToDB(enrichment=False)
    #test.getKeyWordsFromTweets()
    #test.renameFiles()
    #test.treatFiles()
    test.lanchInsertionToIntermediaryDB2()
    #test.getDistinctTweets()