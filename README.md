

  Assignment 2
============

## Sentiment Analysis on Twitter Posts 


1.	Introduction
2.	Tweet Extraction
3.	Sentiment Analysis
4.	Loading data into Elastic Search DB

---
###### Introduction

In this problem, set of tweets is to be extracted from the twitter database and then sentiment analysis is performed on it, in order to find polarity (positive, negative or neutral emotion) of the tweets. Finally, dataset created from the sentiment analysis is to be uploaded on the elastic search cloud platform.     

###### Tweet Extraction

Tweet can be extraxted in the following order: 
1.	Connecting to the twitter API 
2.	Authentication
3.	Saving tweets to csv

Result is stored on to tweets121.csv file.

###### Sentiment Analysis
	
As tweets are unstructured form of data, it needs to be preprocessed before analysing.
Preprocessing is done in many phases :
•	Remove html links from the tweets 
•	Remove retweet entities 
•	Remove all hashtags 
•	Remove all @people
•	Remove all punctuation 
•	Remove all numbers 
•	Remove all unnecessary white spaces  
•	Convert all text into lowercase and 
•	Remove duplicates 
     
Sentiment Analysis is also performed in phases, algorithm can be devised as:
	
1.	Start with downloading and caching the sentiment dictionary 
2.	Download twitter testing data sets, input it in to the program  
3.	Clean the tweets by removing the stop words 
4.	Tokenize each word in the dataset and feed in to the program 
5.	For each word, compare it with positive sentiments and negative sentiments word in the dictionary. Then increment positive count or negative count 
6.	Finally, based on the positive count and negative count, we can get result percentage about sentiment to decide the polarity 

###### Loading Data into Elasticsearch DB

Elastic Search Cloud plateform is used with the basic functionalities to upload the results obtained on to cloud. 


###### Note 

Code snippets are combined and stored in main.py file.
Dictionary files used to compare sentiment and decide score are stored in lexicon_dictionary directory.
tweets_senti53.csv file is the output file after extracting polarity of tweets.