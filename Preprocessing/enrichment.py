from Preprocessing.tweetsExtraction import TweetsRest
from Preprocessing.tweetsInsertionToDB import TweetsInsertionToDB
from Preprocessing.twitterAuthentification import TwitterAuthenticator


class Enrichment():


    def enrich(self,tagsLis):
        twitterAuthentificator = TwitterAuthenticator()
        tweetsRest = TweetsRest(twitterAuthentificator.auth)
        # we have to pass 'True' in case of enrichment
        tweetsRest.extractTweets(tagsList, enrichment=True)
        #we have insert the new tweet into our data warehouse
        dataInsertion = TweetsInsertionToDB()
        # we have to pass 'True' in case of enrichment
        dataInsertion.lanchInsertionToDB(enrichment=True)

if __name__=='__main__':
    tagsList = ['corona', 'coronavirus', 'COVID-19', 'COVID19']
    test = Enrichment()
    test.enrich(tagsList)
