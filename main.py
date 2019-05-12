import time
import csv
import nltk
import re
import tweepy
import String

from nltk.corpus import stopwords
from string import digits
from elasticsearch import Elasticsearch
from datetime import datetime
from elasticsearch import helpers

nltk.download('stopwords')

english_stops=set(stopwords.words('english'))

Consumer_Key="rw8OFjMXtMA8JmaoTAOUNlYL6"
Consumer_Secret="40r77o4fN2zjMlJjMVF3m1VSZArPTZDhFX7fbv6uHgwwCqQ5Y7"
Access_Token="1044740282544267264-tg7yVJt7oCHJn3YMKXODWffStqjPzU"
Access_Secret="ysGGpeyS2AAqRLvHcUQDKscPsvQt7q9SyLUTe0oAW0QwF"

auth=tweepy.OAuthHandler(Consumer_Key,Consumer_Secret)
auth.set_access_token(Access_Token,Access_Secret)
api=tweepy.API(auth)


def get_tweets(query):
    api=tweepy.API(auth)
    try:
        tweets=api.search(query)
    except tweepy.error.TweepError as e:
        tweets=json.loads(e.response.text)
    return tweets

	
	
queries=["#mothers","#Protest","#Trees","Black","One plus","California","San jose","#TreatyDay","#FightFor15","#nowwhatott","\"Nova Scotia\"","\"Canada\"","\"Ontario\"","#hfxtransit","#GOT",
         "#Friends","#Trump","\"United States of America\"","#SDLive","#Toronto","#Calagry","#Vancouver","Khabib",
         "James Gunn","#TravelTuesday","#TuesdayThoughts","#TuesdayMotivation","#nspoli","Pixel 3","#yegcc",
         "#FirePreventionWeek2018","Pixel Slate","\"New York\"","\"Harvard\"","\"Chicago\"","\"Miami\"","\"UK\"","\"London\"",
        "#power","#Apple","#Twitter","Microsoft","Adobe","SAP","Ferrari","BMW","SUV","cars","Electronics","mobiles",
        "laptop","hp","lenovo","keys","#HappyNavratri","#AMAs","#GoLeafsGo","#CityofPG","#NewAmsterdam","#GoJetsGo","#MOTWTour",
        "city","states","country","Asia","Europe","North America","America","South America","Central America","electricity","water",
        "dam","dog","cat","animals","save","poor","economy","rich","loans","debt","hollywood","#Avengers","heroin","patner","proud",
        "young","guys"]

#Writing the tweets that we retrieve from Tweeter

with open('tweets121.csv','w',encoding="utf-8") as outfile:
    writer=csv.writer(outfile)
    writer.writerow(['id','user','created_at','text'])
              
    for query in queries:
        t=get_tweets(query)
        for tweet in t:
            writer.writerow([tweet.id_str,tweet.user.screen_name,tweet.created_at,tweet.text])
			

#Creating a Dictionary in the Python using Lexicons
			
with open('convertcsv_forme.csv',mode='r') as infile:
    reader1=csv.reader(infile)
    with open('convertcsv_forme_new2.csv',mode='w') as outfile:
        writer1=csv.writer(outfile)
        mydict={rows[0]:rows[1] for rows in reader1}
		
		
with open('tweets_senti53.csv','w',encoding="utf-8") as outfile:
    writer1=csv.writer(outfile)
    writer1.writerow(['text','Sentiment','Sentiment_Score'])
                    
    for query in queries:
        t=get_tweets(query)
        
        for tweet in t:
			#Remove the special characters from the tweet
            cleanString=re.sub('\W+',' ',tweet.text)
            low=cleanString.lower()
			
			#Remove the digits from the tweet			
            remove_all_digits=low.maketrans('','',digits)
            clean_text=low.translate(remove_all_digits)
            
            lists=clean_text.split()
			#Remove the propositions from the tweet
            list=[word for word in lists if word not in english_stops]
            
            sentence_sum=0.0
            
            for lis in list:
                #print(lis+"="+word_avai+"=")
                for word_avai in mydict.keys():    
                    #print(lis+"=="+word_avai)
                    if(lis == word_avai):
                        #str1=int(mydict[word_avai])
                        sentence_sum=float(mydict.get(word_avai))+sentence_sum
                        #print("*"+lis+"="+mydict[word_avai])
                        
                        break
                                    
                
            #print('sentiment of tweet->',sentence_sum,'\n')
			
			#Deciding the Sentiment of the Tweet
            if sentence_sum > 0.0 :
                senti='Positive'
            elif sentence_sum < 0.0 :
                senti='Negative'
            else :
                senti='Neutral'
                
			#Writing the sentiment and sentiment score in CSV file
            writer1.writerow([tweet.text,senti,sentence_sum])
			
			
			
			
#Uploading CSV file in elastic Search using python
es10=Elasticsearch(
                ['portal-ssl1083-26.bmix-dal-yp-5416b83e-7b28-47ed-961b-7f778b204245.111114948.composedb.com'],
                http_auth=('admin','SBNLYCYOEVEIZYVS'),
                port=58101,
                use_ssl='true',
            )
with open('tweets_senti53.csv','r',encoding="utf8") as outfile:
    readerOfCsv=csv.DictReader(outfile)
    helpers.bulk(es10, readerOfCsv, index="index_name_main", doc_type="type")
            