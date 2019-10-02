import re
import tweepy,csv
from tweepy import OAuthHandler
from textblob import TextBlob

class TwitterClient:
    '''
    Generic Twitter Class for sentiment analysis.
    '''

    def __init__(self):
        self.tweets=[]
        self.tweetText=[]

    def downloaddata(self):

        consumer_key = "CFMTW4TrcZmIYHOX9N0zdsfTx"
        consumer_secret = "6Xflj0VCitnBi3QqeenHJUgtgIhndNCRpgnQfAnf4XHiPsDFhJ"
        access_token = "377193754-Ib8aXw4gBrFgOUjdTeqE2ZkBrEGZDXwaQRdkMBWN"
        access_token_secret= "coP73Hs3OhhurQ32tdQ54xfHJkHWGPIMDnXJRYfwjYTNn"
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api= tweepy.API(auth)

        searchTerm = input("Enter Keyword/Tag to search about: ")
        NoOfTerms = int(input("Enter how many tweets to search: "))

        # searching for tweets
        self.tweets = tweepy.Cursor(api.search, q=searchTerm, lang="en").items(NoOfTerms)

        # Open/create a file to append data to
        csvFile = open('result.csv', 'a')

        # Use csv writer
        csvWriter = csv.writer(csvFile)

        # creating some variables to store info
        polarity = 0
        positive = 0
        negative = 0
        neutral = 0

        for tweet in self.tweets:
            # Append to temp so that we can store in csv later. I use encode UTF-8
            self.tweetText.append(self.clean_tweet(tweet.text).encode('utf-8'))
            # print (tweet.text.translate(non_bmp_map))    #print tweet's text
            analysis = TextBlob(tweet.text)
            # print(analysis.sentiment)  # print tweet's polarity
            polarity += analysis.sentiment.polarity  # adding up polarities to find the average later

            if (analysis.sentiment.polarity == 0):  # adding reaction of how people are reacting to find average later
                neutral += 1
            elif (analysis.sentiment.polarity > 0 and analysis.sentiment.polarity <= 1):
                positive += 1
            elif (analysis.sentiment.polarity > -1 and analysis.sentiment.polarity <= 0):
                negative += 1


            # Write to csv and close csv file
        csvWriter.writerow(self.tweetText)
        csvFile.close()

        # finding average of how people are reacting
        positive = self.percentage(positive, NoOfTerms)
        negative = self.percentage(negative, NoOfTerms)
        neutral = self.percentage(neutral, NoOfTerms)

        # finding average reaction
        polarity = polarity / NoOfTerms

        # printing out data
        print("How people are reacting on " + searchTerm + " by analyzing " + str(NoOfTerms) + " tweets.")
        print()
        print("General Report: ")

        if (polarity == 0):
            print("Neutral")
        elif (polarity > 0 and polarity <= 1):
            print("Positive")
        elif (polarity > -1 and polarity <= 0):
            print("Negative")

        print()
        print("Detailed Report: ")
        print(str(positive) + "% people thought it was positive")
        print(str(negative) + "% people thought it was negative")
        print(str(neutral) + "% people thought it was neutral")



    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])| (\w+:\ / \ / \S+)", " ", tweet).split())

    def percentage(self,part,whole):
        temp = 100 * float(part) / float(whole)
        return format(temp, '.2f')


if __name__=="__main__":
    sa=TwitterClient()
    sa.downloaddata()



