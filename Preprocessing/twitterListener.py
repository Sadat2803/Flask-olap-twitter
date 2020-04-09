from tweepy import StreamListener

class TwitterListener(StreamListener):

    def __init__(self, tweetsFilename):
        self.tweetsFilename = tweetsFilename

    def on_data(self, data):
        try:
            print(data)
            tweetsFile = open(self.tweetsFilename, 'a')
            tweetsFile.write(data)
            return True
        except BaseException as e:
            print("Error : %s" % str(e))
        return True

    def on_error(self, status):
        if status == 420:
            # when rate limit occurs.
            return False
        print(status)
