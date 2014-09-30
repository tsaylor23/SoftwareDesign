# -*- coding: utf-8 -*-
"""
ferguson.py
date created: 9/29/2014

 A script to mine data from Twitter, and gather information
 about their filtering of news and commentary on the happenings in Ferguson,
 Missouri.
 
author= Toni Saylor
"""

from pattern.web import *
import sys
import time
import matplotlib.pyplot as plt

# intitialize vectors
# tweets holds the total number of tweets made in 60 seconds, made in 10 
# minutes
tweets = []
# statuses holds the total number of statuses made in 60 seconds, made in 10 
# minutes
statuses = []
# timet is in array of the time in seconds for each search of twitter and
# facebook
timet = [60,120,180,240,300,360,420,480,540,600]
# I run my code to pull the number of statuses and tweets 10 times to get 
# 10 data points. This means my code runs for 10 minutes
for n in range(10):
    # initialize s_old as an empty string
    s_old=''
    # intitialize the total number of tweets as an empty array
    list_tweets=[]
    
    # searches twitter for posts containing the word Ferguson. I decided
    # not to just search for the #Ferguson, just in case people were 
    # mentioning it but not hashtagging.
    s = Twitter().stream('Ferguson')
    # for 60 seconds I search twitter for incoming posts about Ferguson
    for i in range(60):
        # allows it to search every second, rather than every millisecond
        # or something
        time.sleep(1)
        s.update(bytes=1024)
        # if the tweet before is the same as the next one, I don't print the
        # next one 
        if s and s[-1].text!=s_old:
             # store the text of s[-1]
             s_old = s[-1].text
             # add the tweet to an array of strings containing the tweets
             list_tweets.append(s_old)
    print ('The total number of posts from Twitter is:')
    # the length of the list of tweets is the amount of tweets made
    print len(list_tweets)
    # appends the number of tweets to tweets
    tweets.append(len(list_tweets))

    
    list_statuses=[]
    # Signing in to my facebook
    fb = Facebook(license='CAAEuAis8fUgBAFaC8FXH0Y7BY8LsM80tHwRCXs8F5Gp1xrhJVpe81J8aZCpvzFWq2crPRq0FZCOCSsWm0D9e4f08qkWjvwKUZA5e2AX8hK5vMMpBFXVmbp3BaCZBxtn14sXCBayzIyj3FDI8aBrlQcsHJN8x43BxrzSXcyKPqaiLnbE70bhLBefPtO0fZCnMZD')
    # for each post in fb, search for Ferguson, Missouri for up to 1000 posts
    for post in fb.search('Ferguson,Missouri', type=SEARCH, count=1000):
        list_statuses.append(post.text)
        # .get('date') gets the timestamp of the post. Then I split it to make
        # it more legible. The result is time in h:min:sec    
        post_time = post.get('date').split('T')[1].split('+')[0]
        # I get the time according to my computer and make it legible
        my_time=time.ctime().split(' ')[3]
        # I convert the times into a number of seconds, and for the post time I 
        # add 20 hours, because for some reason the time is 20 hours off for 
        # them all.
        post_time_raw=3600*(20+int(post_time.split(':')[0]))+60*int(post_time.split(':')[1])+int(post_time.split(':')[2])
        my_time_raw=3600*int(my_time.split(':')[0])+60*int(my_time.split(':')[1])+int(my_time.split(':')[2])
        # if the post time is 1 minute older than my time, I break so that I 
        # only get 1 minutes worth of data.    
        if (post_time_raw+(60)) < my_time_raw:
            break

    print ('The total number of posts from facebook is:')
    print len(list_statuses)
    # adds the number of statuses to statuses
    statuses.append(len(list_statuses))

print tweets
print statuses
#time_tweets = []

# using matplotlib I plot a graph of tweets and statuses versus times
plt.plot(timet, tweets, 'r', timet, statuses, 'b')
plt.axis([60,600, 0, 70])
plt.title('Tweets and Statuses versus Time')
plt.xlabel('Time (s)')
plt.ylabel('Tweets (red) and Statuses (blue)')

        
