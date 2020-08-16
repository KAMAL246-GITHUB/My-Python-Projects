########################################################################################################
###  This project lists the top 10 banks retrieved from Investopedia through webscraping.            ###
###  It collects all the tweets which mention the name of these banks using Twitter API/ Endpoints   ###
###  Then it uses the textblob library to calculate the polarity of the sentiment (ranging from      ###
###  -1 to +1) expressed by each tweet. Finally it calculates the average sentiment polarity and     ###
###  plots a horizontal bar chart to show the sentiment score of all the banks.                      ###
########################################################################################################

import tweepy
import Twitter_Credentials as tc # API keys are stored in Twitter_Credentials.py and imported here
import Top_Banks_Of_World as tbw # Top_Banks_Of_World is a script which scrapes web to find a list top10 banks
import pandas as pd
import matplotlib.pyplot as plt
from textblob import TextBlob
import re
%matplotlib inline


#Assign Secret Keys placed in Twitter_Credentials.py file

CONSUMER_KEY = tc.CONSUMER_KEY
CONSUMER_SECRET = tc.CONSUMER_SECRET
ACCESS_TOKEN = tc.ACCESS_TOKEN
ACCESS_TOKEN_SECRET = tc.ACCESS_TOKEN_SECRET

# Authenticate to Twitter

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN,ACCESS_TOKEN_SECRET)

# Create API object
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


def clean_tweet(tweet):
    '''
    This function cleans tweet text(passed in as argument) by removing links,
    special characters etc, using regex statements from re package.
    
    '''
    
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|\
    (\w+:\/\/\S+)", " ", tweet).split())  
#"\" at the end of the middle line is used for line break not a part of regex


def get_tweet_sentiment(tweet):
        '''
        This function classifies the overall sentiment of a given tweet(provided as input) using TextBlob library.
        It returns a sentiment polarity number (ranges from -1 to +1)
        '''
        analysis = TextBlob(clean_tweet(tweet)) # Make TextBlob object
        return analysis.sentiment.polarity  # return sentiment score


def Tweet_Sentiment(Search_String):
    '''
    This function reads data from Twitter using tweepy based on the input search string.
    In this case the searchstring will be the name of the bank from the top 10 list.
    It calls other previously defined functions to get the sentiement scores.
    ''' 
    Search_String_Final = Search_String + ' -filter:retweets'
    
    #Fetch Twitter data and process
    ## Provide the past date since when you want to analyse(since =<date>). The tweetsitems() can take argument 
    # It wil be the number of tweets you want to pull. Tweet_mode - extended ensures the complete tweet text is retrieved.

    sentiment_score = 0
    for tweet_info in tweepy.Cursor(api.search, q = Search_String_Final, \
                                    since='2019-12-26', \
                                    tweet_mode = "extended").items(): 
        sentiment_score += get_tweet_sentiment(tweet_info.full_text)
    return [Search_String, sentiment_score]


def Sentiment_BarChart():
    '''
    This function makes a pandas dataframe wit the values returned by Tweet_Sentiment function.
    One column is the bank name and the other is the sentiment score.
    Then it uses matplot library to plot a horizontal bar chart.
    '''
    Sentiment_List = [Tweet_Sentiment(bank) for bank in tbw.Top_Bank_List]
    Bank_Frame = pd.DataFrame(data = Sentiment_List,
                             columns = ['Bank Name', 'Sentiment Score'])
    # Plot horizontal bar graph
    fig, ax = plt.subplots(figsize=(15, 8))
    
    Bank_Frame.plot.barh(color='red', x='Bank Name', y='Sentiment Score',ax=ax)
    ax.set_title("Top Banks Tweet Sentiment Analyis\n\n", fontsize = 20 )

    plt.legend(frameon = False, fontsize = 13)
    plt.tick_params(bottom= False, left = False, labelsize = 13)
    plt.style.use('bmh')
    plt.xlabel('\nSentiment Score', fontsize = 15)
    plt.ylabel('Bank Name\n', fontsize = 15)
    plt.box(False)

    plt.show()

if __name__ == '__main__':
    Sentiment_BarChart()
