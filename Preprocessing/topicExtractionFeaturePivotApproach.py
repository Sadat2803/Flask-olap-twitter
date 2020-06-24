import collections
import json
import operator
import re
from collections import defaultdict
from os import listdir
from os.path import isfile, join
import textdistance

import mysql.connector
import preprocessor as p
from nltk.corpus import stopwords
from textblob import TextBlob

from IntermediaryDB.allTweets import AllTweets
from Preprocessing.tweetsPreProcessing import TweetsPreProcessing



class TopicExtractionFeaturePivotApproach():

    def insertTweetsIntoDB(self):
        concept = "coronavirus"
        analysisID = "passif"

        preProcessing = TweetsPreProcessing()
        dirPath = "C:/Users/Raouf/PycharmProjects/PFE_SII_M2/TweetFiles/"

        allFiles = [f for f in listdir(dirPath) if isfile(join(dirPath, f))]
        print(allFiles)
        for fileName in allFiles[63:]:
            print(fileName)
            if fileName.startswith("ExtractedTweetsFor"):
                if not fileName.endswith("Loaded.json"):  # check if the file is loaded to the database or not
                    fullFileName = dirPath + fileName
                    tweetsFile = open(fullFileName, 'r', encoding="utf-8")
                    tweets = json.load(tweetsFile)

                    cpt = 0
                    for tweet in tweets['tweets']:
                        tweetLanguage = tweet['lang']
                        if tweetLanguage == "en":
                            allTweets = AllTweets()
                            tweetID = tweet['id_str']
                            parsed_tweet = p.parse(tweet['text'])
                            hashtagsList = parsed_tweet.hashtags
                            print(hashtagsList)
                            hashtagsText = ""
                            if hashtagsList!= None:
                                for hashtag in hashtagsList:
                                    print(hashtag.match)
                                    hashtagsText += " "+ str(hashtag.match)
                            text = p.clean(tweet['text'])
                            text = " ".join(re.findall('\w+', text))
                            text += ", hashtags : "+hashtagsText
                            #text = "text"
                            row = [tweetID, text]
                            row += preProcessing.getLangage(tweet['lang']) + preProcessing.getLocation(
                                tweet['user']['location']) \
                                   + preProcessing.getTime(tweet['created_at']) + preProcessing.getSentimentAnalysis(
                                tweet['text']) \
                                   + preProcessing.getSource(tweet['source'])
                            row += [analysisID, concept]
                            #print(row)
                            try:
                                allTweets.insert(row)
                                cpt += 1
                                print(cpt, "tweets ", sep=" ")
                            except:
                                print("erreur encodage")

                    print("For the file : ", fileName, ", Tweets number is : ", cpt)
                    tweetsFile.close()

    def featurePivotApproach(self, analysisID):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="interDB"
        )
        mycursor = mydb.cursor()
        query = "select text, tweetID from alltweets where languageCode = 'en' and analysisID = '" + analysisID + "'"
        mycursor.execute(query)
        result = mycursor.fetchall()

        stopWords = set(stopwords.words('english'))
        customizedStopWords = {'rt', 'hashtags', 'retweet', 'said','total','gmt','video','hum','read','trend',
                               'update','updates','day','today','news','num','sky','th'}
        stopWords = stopWords.union(customizedStopWords)

        #step 1 and 2 : create unigrams from the tweets
        unigramsList = list()
        unigramsSet = set()
        unigramsFrequency = defaultdict(int)
        associatedTweetsForUnigramsSet = defaultdict(lambda: set())
        unigramsByTweetID = defaultdict(lambda: set())
        for row in result:
            tweetText = row[0].lower()
            print(tweetText)
            #tweetText = tweetText[:tweetText.index("hashtags")-2] # use only hashtags and not the hole tweet
            tweetID = row[1]
            #blob = TextBlob(tweetText)
            #tempList = tweetText.split(" ")
            tokens = re.findall("[a-zA-Z_]{2,}[ ][a-zA-Z_]{2,}", tweetText)
            #print(tokens)
            for token in tokens:
            #for token in tokens:
                temp = token.split(" ")
                word1 = temp[0]
                word2 = temp[1]
                if (word1 not in stopWords) and (word2 not in stopWords):
                    """for word in unigramsSet:
                        # pour le cas erreur de saisie du mot
                        distanceLevenshtein = textdistance.levenshtein(word, noun)
                        print("leven Distance : ",word," ",noun," ",distanceLevenshtein)
                        # pour calculer la distance phonitique
                        distanceMRA = textdistance.mra(word, noun)
                        print("MRA Distance : ", word, " ", noun, " ", distanceMRA)"""
                    unigramsList.append(token)
                    unigramsSet.add(token)
                    associatedTweetsForUnigramsSet[token].add(tweetID)
                    unigramsFrequency[token] += 1
                    unigramsByTweetID[tweetID].add(token)
        #print(unigramsList.__len__())
        #print(unigramsSet.__len__())

        #step 3 : calculate the avg frequency
        sommeOfFrequencies = 0
        for unigram in unigramsSet:
            sommeOfFrequencies += unigramsFrequency[unigram]
        averageFrequency = round(sommeOfFrequencies / unigramsSet.__len__())

        #step 4 :
        #first we have to order the frequencies of unigrams in descending order
        unigramsFrequency = dict(sorted(unigramsFrequency.items(), key=operator.itemgetter(1), reverse=True))
        print(unigramsFrequency)
        significantUnigramsSet = list()
        for unigram in unigramsFrequency:
            """if significantUnigramsSet.__len__()>=20:
                break"""
            if unigramsFrequency[unigram] >= averageFrequency:
                significantUnigramsSet.append(unigram)
        print(significantUnigramsSet)
        #step 5 : get the associated tweets for every significant unigram
        associatedTweetsForSignificantUnigramsSet = defaultdict(lambda: set())
        setOfTotalSetOfTweets = list()
        for unigram in significantUnigramsSet:
            setOfTotalSetOfTweets.append(associatedTweetsForUnigramsSet[unigram])

        #step 6 : calculate proportinal frequency for each unigram d(i,l)
        unigramsForAssociatedTweetsSets = list()
        for setOfTweets in setOfTotalSetOfTweets:
            #temp : contains all the unigrams from the tweets which have th id 'tweetID'
            temp = set()
            for tweetID in setOfTweets:
                temp = temp.union(unigramsByTweetID[tweetID])
            unigramsForAssociatedTweetsSets.append(list(temp))

        proportionalFrequencies = list()
        for unigramsForAssociatedTweetsSet in unigramsForAssociatedTweetsSets:
            sommeOfFrequencies = 0
            for unigram in unigramsForAssociatedTweetsSet:
                sommeOfFrequencies += unigramsFrequency[unigram]
            temp = list()
            for unigram in unigramsForAssociatedTweetsSet:
                proportionalFrequency = unigramsFrequency[unigram] / sommeOfFrequencies
                temp.append(proportionalFrequency)
            proportionalFrequencies.append(temp)

        #step 7 : calculate the average proportional frequency for each set of aasociated tweets
        averageProportionalFrequencies = list()
        for listProportinalFrequencies in proportionalFrequencies:
            sommeOfFrequencies = 0
            for proportinalFrequency in listProportinalFrequencies:
                sommeOfFrequencies += proportinalFrequency
            avgPropFreq = sommeOfFrequencies / listProportinalFrequencies.__len__()
            averageProportionalFrequencies.append(avgPropFreq)

        #step 8 and 9 : extract frequent common unigrams
        setOfFrequentCommonUnigrams = list()
        i = 0
        #allTopics = defaultdict(int)
        for listProportinalFrequencies in proportionalFrequencies:
            frequentCommonUnigrams = set()
            j = 0
            for proportionalFrequency in listProportinalFrequencies:
                if proportionalFrequency >= averageProportionalFrequencies[i]:
                    frequentCommonUnigrams.add(unigramsForAssociatedTweetsSets[i][j])
                    """pf = allTopics.get(unigramsForAssociatedTweetsSets[i][j], 0)
                    if pf < proportionalFrequency:
                        allTopics[unigramsForAssociatedTweetsSets[i][j]] = proportionalFrequency"""
                j += 1
            setOfFrequentCommonUnigrams.append(frequentCommonUnigrams)
            i += 1
        #---------------------------------------------
        """allTopics = dict(sorted(allTopics.items(), key=operator.itemgetter(1), reverse=True))
        numberOfTopics = 50
        cpt = 0
        print(allTopics)
        outputList = []
        for topic in allTopics:
            outputList.append(topic)
            if cpt > numberOfTopics:
                break
            cpt += 1
        return outputList"""
        #---------------------------------------------


        #step 10 : application of the "content similarity" algorithm
        theta1 = 0.3
        theta2 = 0.2
        beta = 20
        topics = [] #it is a list of lists of unigrams
        s = significantUnigramsSet.__len__()
        i = 0
        #allTopics = []
        while i <= s - 3:
            unigramI = significantUnigramsSet[i]
            if not self.includeIn(unigramI, topics):
                topic = set()
                topicTweets = set()
                topic.add(unigramI)
                topicTweets = topicTweets.union(associatedTweetsForUnigramsSet[unigramI])
                j = i + 1
                while j <= s - 2:
                    unigramJ = significantUnigramsSet[j]
                    if not self.includeIn(unigramJ, topics):
                        FCUi = setOfFrequentCommonUnigrams[i]
                        FCUj = setOfFrequentCommonUnigrams[j]
                        if self.jaccard(FCUi, FCUj) >= theta1:
                            topic.add(unigramJ)
                            topicTweets = topicTweets.union(associatedTweetsForUnigramsSet[unigramJ]) - \
                                          topicTweets.intersection(associatedTweetsForUnigramsSet[unigramJ])
                            k = j + 1
                            while k <= s - 1:
                                unigramK = significantUnigramsSet[k]
                                if not self.includeIn(unigramK, topics):
                                    FCUj = setOfFrequentCommonUnigrams[j]
                                    FCUk = setOfFrequentCommonUnigrams[k]
                                    if self.jaccard(FCUj, FCUk) >= theta2:
                                        topic.add(unigramK)
                                        topicTweets = topicTweets.union(associatedTweetsForUnigramsSet[unigramK]) - \
                                                      topicTweets.intersection(associatedTweetsForUnigramsSet[unigramK])
                                k += 1
                    j += 1
                if topicTweets.__len__() >= beta:
                    #print("Topic : ", topic)
                    topics.append(list(topic))
                    #allTopics.append(topic)
                    #break
                    #print("TopicTweets : ",topicTweets)
            i += 1
        #print(allTopics)
        #print(unigramsFrequency['extends lockdown'])
        #print("---------------------Treatment ---------------------")
        dataList = []
        element = {'word': '', 'frequency': 0}
        for topic in topics:
            #print(topic)
            mostFrequentWord = topic[0]
            for word in topic:
                if unigramsFrequency[mostFrequentWord] < unigramsFrequency[word]:
                    mostFrequentWord = word
            element['word'] = mostFrequentWord
            element['frequency'] = unigramsFrequency[mostFrequentWord]
            dataList.append(element)
            element = {'word': '', 'frequency': 0}

        return dataList

    def includeIn(self, unigram, topics):
        for topic in topics:
            if unigram in topic:
                return True
        return False

    def jaccard(self, FCUi, FCUj):
        intersection = FCUi.intersection(FCUj).__len__()
        union = FCUi.union(FCUj).__len__()
        if union != 0:
            return intersection/union
        else:
            return 0


if __name__ == "__main__":
    test = TopicExtractionFeaturePivotApproach()
    #test.insertTweetsIntoDB()
    test.featurePivotApproach()
