
import re
from datetime import date
import requests
from iso639 import languages
import nltk
from textblob import TextBlob
import preprocessor as p
import cv2 as cv
import gender_guesser.detector as gender

class TweetsPreProcessing():
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
    continentsCode = {
        'North America': 'NA',
        'South America': 'SA',
        'Asia': 'AS',
        'Australia': 'OC',
        'Africa': 'AF',
        'Europe': 'EU'
    }



    def getTime(self,fullCreationDate):

        day = fullCreationDate[8:10]
        month = self.monthList[fullCreationDate[4:7]]
        year = fullCreationDate[26:31]
        """
        hour = fullCreationDate[11:13]
        minute = fullCreationDate[14:16]
        """
        timeAltID = year+month+day#+hour+minute
        dayOfWeek = fullCreationDate[0:3]
        monthName = fullCreationDate[4:7]
        """morning = range(6,12)
        afternoon = range(12,18)
        evening = range(18,21)

        if int(hour) in morning:
            periodeOfDay = 'morning'
        elif int(hour) in afternoon:
            periodeOfDay = 'afternoon'
        elif int(hour) in evening:
            periodeOfDay = 'evening'
        else:
            periodeOfDay = 'night'
        """

        dayOfYear =  date.fromisoformat(year+'-'+month+'-'+day).timetuple().tm_yday
        spring = range(80, 172)
        summer = range(172, 264)
        autumn = range(264, 355)
        if dayOfYear in spring:
            season = 'spring'
        elif dayOfYear in summer:
            season = 'summer'
        elif dayOfYear in autumn:
            season = 'autumn'
        else:
            season = 'winter'

        return [timeAltID, dayOfWeek, day, month, monthName, year, season]

    def getLangage(self,languageCode):
        if languageCode in["und","in","iw"]:
            languageCode = "und"
            languageName = "und"
        else:
            languageName = languages.get(alpha2= languageCode).name

        return [languageCode, languageName]

    def getSentimentAnalysis(self,text):
        #clean the the txeet text by removing links and special characters
        text = p.clean(text)
        myText = TextBlob(text)
        if myText.sentiment.polarity>0:
            sentimentLabel='positive'
        elif myText.sentiment.polarity==0:
            sentimentLabel = 'neutral'
        else:
            sentimentLabel = 'negative'
        sentimentValue = myText.sentiment.polarity

        return [sentimentValue, sentimentLabel]

    def getSource(self,fullSource):

        temp = re.findall(r'<.+>(.+)</a>',fullSource)
        try:
            sourceTokens = temp[0].split()
        except:
            sourceTokens = ""
        iPhoneTokens = ['iphone','ipad' , 'ios']
        androidTokens = ['android']
        webTokens = ["web","mac","google"]

        sourceName = 'Unknown'
        for token in sourceTokens:
            if token.lower() in iPhoneTokens:
                sourceName = 'iPhone'
                break
            if token.lower() in androidTokens:
                sourceName = 'Android'
                break
            if token.lower() in webTokens:
                sourceName = 'Web'
                break
        return [sourceName]

    def getLocation(self,location):

        import pickle
        with open('../Docs/locations.pickle', 'rb') as file:
            worldCitiesDict = pickle.load(file)
            worldIso2Dict = pickle.load(file)
            worldIso3Dict = pickle.load(file)
            worldCountriesDict = pickle.load(file)
        if location == None: #in case no location given by the user
            location=""
        en_blob = TextBlob(location)
        """try:
            en_blob.translate(to='en')
            location = en_blob.string
        except NotTranslated or TranslatorError:
            pass"""
        #translator = Translator()
        #location = translator.translate(location, dest='en')
        try:
            location = location.lower()
        except: # in case we try for example to manipulate arabic letters
            pass
        pattern = r'[a-zA-äöüéệć]+'

        #create unigram bigrams trigrams
        locationTokensUnigram = nltk.tokenize.regexp_tokenize(location,pattern)
        locationTokensBigrams = [ word1+" "+word2 for (word1,word2) in list(nltk.bigrams(locationTokensUnigram))]
        locationTokensTrigrams = [ word1+" "+word2+" "+word3 for (word1,word2,word3) in list(nltk.trigrams(locationTokensUnigram))]

        city = "ND"
        country = "ND"
        iso2 = "ND"
        iso3 = "ND"
        continentID = "ND"
        continent = "ND"
        boolean = False
        #--------------------search for the city-----------------------#
        # search with unigram first
        for temp in locationTokensUnigram:
            if worldCitiesDict.get(temp,False)!=False:
                city = temp
                country = worldCitiesDict[temp]
                iso2 = worldIso2Dict[country]
                iso3 = worldIso3Dict[country]
                continent = worldCountriesDict[country]
                continentID = self.continentsCode[continent]
                boolean = True
                break
        if boolean == False:
            # search with bigrams
            for temp in locationTokensBigrams:
                if worldCitiesDict.get(temp, False) != False:
                    city = temp
                    country = worldCitiesDict[temp]
                    iso2 = worldIso2Dict[country]
                    iso3 = worldIso3Dict[country]
                    continent = worldCountriesDict[country]
                    continentID = self.continentsCode[continent]
                    boolean = True
                    break
        if boolean==False:
            # search with trigrams
            for temp in locationTokensTrigrams:
                if worldCitiesDict.get(temp, False) != False:
                    city = temp
                    country = worldCitiesDict[temp]
                    iso2 = worldIso2Dict[country]
                    iso3 = worldIso3Dict[country]
                    continent = worldCountriesDict[country]
                    continentID = self.continentsCode[continent]
                    boolean = True
                    break
        # --------------------search for the full name country in case city not found-----------------------#
        if boolean == False:
            # search with unigram
            for temp in locationTokensUnigram:
                if worldCountriesDict.get(temp, False) != False:
                    country = temp
                    iso2 = worldIso2Dict[temp]
                    iso3 = worldIso3Dict[temp]
                    continent = worldCountriesDict[temp]
                    continentID = self.continentsCode[continent]
                    boolean = True
                    break
        if boolean==False:
            # search with bigrams
            for temp in locationTokensBigrams:
                if worldCountriesDict.get(temp, False) != False:
                    country = temp
                    iso2 = worldIso2Dict[temp]
                    iso3 = worldIso3Dict[temp]
                    continent = worldCountriesDict[temp]
                    continentID = self.continentsCode[continent]
                    boolean = True
                    break
        if boolean==False:
            # search with trigrams
            for temp in locationTokensTrigrams:
                if worldCountriesDict.get(temp, False) != False:
                    country = temp
                    iso2 = worldIso2Dict[temp]
                    iso3 = worldIso3Dict[temp]
                    continent = worldCountriesDict[temp]
                    continentID = self.continentsCode[continent]
                    boolean = True
                    break
        # --------------------search for the iso3 country in case city and full name country not found-----------------------#
        if boolean == False:
            # search with unigram
            for temp in locationTokensUnigram:
                if worldIso3Dict.get(temp, False) != False:
                    country = worldIso3Dict[temp]
                    iso2 = worldIso2Dict[country]
                    iso3 = temp
                    continent = worldCountriesDict[country]
                    continentID = self.continentsCode[continent]
                    boolean = True
                    break
        # --------------------search for the iso2 country in case city and full name and iso3 country not found-----------------------#
        if boolean == False:
            # search with unigram
            for temp in locationTokensUnigram:
                if worldIso2Dict.get(temp, False) != False:
                    country = worldIso2Dict[temp]
                    iso2 = temp
                    iso3 = worldIso2Dict[country]
                    continent = worldCountriesDict[country]
                    continentID = self.continentsCode[continent]
                    boolean = True
                    break
        # --------------------search for the continent if no one of the informations above are available -----------------------#
        continents = ['North America','South America','Asia','Australia','Africa','Europe']
        if boolean == False:
            # search with unigram
            for temp in locationTokensUnigram:
                for contin in continents:
                    if temp.casefold()==contin.casefold():
                        continent = contin
                        continentID = self.continentsCode[continent]
                        boolean = True
                        break
        if boolean == False:
            # search with bigrams
            for temp in locationTokensBigrams:
                for contin in continents:
                    if temp.casefold() == contin.casefold():
                        continent = contin
                        continentID = self.continentsCode[continent]
                        boolean = True
                        break

        #------------------the final result----------------------#
        if boolean ==True:
            # location found
            pass
            #print("location found")
        else:
            # location not found
            pass
            #print("location not found")

        #print("Unigram :",locationTokensUnigram)
        #print("Bigrams :",locationTokensBigrams)
        #print("Trigrams :",locationTokensTrigrams)
        #print("city :",city)
        #print("iso2 :", iso2)
        #print("iso3 :", iso3)
        #print("country :", country)
        #print("continent :", continent)
        if country == "ND":
            locationAltID = "ND"
        else:
            locationAltID = ''.join(city.split())+iso3
        return [locationAltID, city ,iso2 ,country ,continentID ,continent]



    """def getSexe(self,profileName):
        detectorUS = GenderDetector('us')
        detectorUK = GenderDetector('uk')
        detectorUY = GenderDetector('uy')
        detectorAR = GenderDetector('ar')
        try:
            name = profileName.split()[0]
        except:
            name = profileName
        sexe = 'unknown'

        try:
            sexe = detectorUS.guess(name)
            if sexe =='unknown':
                try:
                    sexe = detectorUK.guess(name)
                    if sexe == 'unknown':
                        try:
                            sexe = detectorUY.guess(name)
                            if sexe == 'unknown':
                                try:
                                    sexe = detectorAR.guess(name)

                                except:
                                    #print("detectorAR can't find:", name, sep=" ")
                                    pass
                        except:
                            #print("detectorUY can't find:", name, sep=" ")
                            pass
                except:
                    #print("detectorUK can't find:",name,sep=" ")
                    pass
        except:
            #print("detectorUS can't find:",name,sep=" ")
            pass

        return sexe
        """


    def getProfilePic(self,picUrl,picID):
        picUrl = picUrl.replace("normal","400x400")
        response = requests.get(picUrl, stream=True)
        if response.ok:
            with open("../images/" + picID + '.jpg', 'wb') as profilePic:
                for block in response.iter_content(1024):
                    if not block:
                        break
                    profilePic.write(block)
        else:
            print("invalid url")


if __name__ == '__main__':
    preProcessing = TweetsPreProcessing()
    loc = preProcessing.getLocation("i live in japan")
    print(loc)
    """tweetsFile = open('Docs/myTweetsExtracted.json', 'r', encoding="utf-8")
    tweets = json.load(tweetsFile)
    cpt = 0
    for tweet in tweets['tweets'][:100]:
        picUrl = tweet['user']['profile_image_url']
        picID = tweet['user']['id_str']
        preProcessing.getProfilePic(picUrl, picID)
    """

    #prof = "i am an engenier"
    #print(preProcessing.getProfession(prof))
    #path = "images/mnanuk.jpg"
    #cv2.imread(path)
    #preProcessing.getGenderAge(path)
    #print(preProcessing.getGenderAge("samir"))
    #print(preProcessing.getSexe("samir"))
    #print(preProcessing.getSentimentAnalysis("i am happy"))
    #print(preProcessing.getLangage('en'))
    #print(preProcessing.getLocation('i am from algiers'))
    #preProcessing.tweetsToDataFrame()
    #print(pd['mois'])
    #lang = languages.get(part1='ru')
    #print(lang.name)


