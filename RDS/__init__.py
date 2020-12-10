import praw
from psaw import PushshiftAPI
import os
import datetime as dt
import pandas as pd
import numpy as np
from tqdm import tqdm
from IPython.display import clear_output
import math
from sympy import *

class RDS:
    def __init__(self,client_id = None,client_secret = None,user_agent = 'anonymous'):

        assert (client_id != None) and (client_secret != None), 'ERROR: You must pass parameters for client_secret and client_id'

        self.data_downloaded = False

        self.client_id = client_id
        self.client_secret = client_secret
            
        # user agent is passed to track what is interacting with the reddit API
        self.user_agent = {'user':user_agent,
                          'application':'Reddit Data Scraper'}
        
        # we instantiate the praw instance so we can pass it into the pushshift API
        self.r = praw.Reddit(client_id = self.client_id,
                            client_secret = self.client_secret,
                            user_agent = self.user_agent)
        
        # we try calling the API once to test that it is actually working, and that the credentials were valid
        try:
            list(self.r.subreddit('python').hot(limit=1))
        except:
            raise Exception('ERROR: Could not connect to Reddit API, please check your credentials')

        self.api = PushshiftAPI(self.r)


        print('Successfully connected to Reddit API')

    def __calc_controversiality(self,upvote_ratio):
        if upvote_ratio < 0.5:
            return upvote_ratio*2
        elif upvote_ratio > 0.5:
            return (upvote_ratio*-2) + 2
        else:
            return 1

	def __calc_votes(self, score, upvote_ratio):
	    if score == 0:
	        return 0,0
	    else:
	        upvotes,downvotes = symbols('x y')
	        ups,downs = list(linsolve([upvotes - downvotes - score, upvote_ratio*(upvotes+downvotes) - upvotes],(upvotes,downvotes)))[0]
	        ups,downs = int(ups),int(downs)
	        return ups, downs

    def __get_single_days_data(self,subreddit,day,limit=100):
        "API limit seems to be 100 right now"
        start = int(dt.datetime(day[0],day[1],day[2]).timestamp())
        end = dt.datetime(day[0],day[1],day[2])+dt.timedelta(days=1)
        end = int(end.timestamp())
        gen = self.api.search_submissions(after=start,
                                      before=end,
                                      subreddit=subreddit,
                                      limit=limit)
        results = list(gen)

        data = {'author':[],
               'created_utc':[],
               'id':[],
               'num_comments':[],
               'score':[],
               'subreddit':[],
               'title':[],
               'upvote_ratio':[],
               'flair':[],
               'url':[],
               'text':[]}

        for result in results:
            data['author'].append(result.author)
            data['created_utc'].append(result.created_utc)
            data['id'].append(result.id)
            data['num_comments'].append(result.num_comments)
            data['score'].append(result.score)
            data['subreddit'].append(result.subreddit)
            data['title'].append(result.title)
            data['upvote_ratio'].append(result.upvote_ratio)
            data['url'].append(result.url)
            data['flair'].append(result.link_flair_text)
            data['text'].append(result.selftext)

        upvote_list = []
        downvote_list = []
        for i in range(len(data['score'])):
            upvotes,downvotes = self.__calc_votes(data['score'][i],data['upvote_ratio'][i])
            upvote_list.append(upvotes)
            downvote_list.append(downvotes)
        

        data['downvotes'] = [int(i) for i in downvote_list]
        data['upvotes'] = [int(i) for i in upvote_list]
        data['controversiality'] = [self.__calc_controversiality(i) for i in data['upvote_ratio']]
        
        data = pd.DataFrame(data).sort_values(by='score',ascending=False).reset_index(drop=True)
        data = data[['created_utc','id','subreddit','author','flair','title','text','score','upvotes','downvotes','upvote_ratio','controversiality','num_comments','url']]
        data.columns = ['posted','id','subreddit','author','flair','title','text','score','upvotes','downvotes','upvote_ratio','controversiality','comments','url']
        return data

    def download(self,subreddit,start,end,limit=100):
        """
        subreddit, str: subreddit you want to gather data from 
        start, tuple: tuple of three ints (year, month, day)
        end, tuple: same format as start
        limit, int: max 100, number of posts for any given day gathered
        """
        # reassign/create date range list
        date_range = (start,end)
        date_range = pd.date_range(start=dt.datetime(date_range[0][0],date_range[0][1],date_range[0][2]),
                           end=dt.datetime(date_range[1][0],date_range[1][1],date_range[1][2])).tolist()
        
        data = pd.DataFrame()
        
        for i in tqdm(date_range):
            data = data.append(self.__get_single_days_data(subreddit,(i.year,i.month,i.day),limit=limit))
            clear_output()
        data['posted'] = data['posted'].apply(dt.datetime.fromtimestamp)
        data['posted'] = data['posted'].astype(str).apply(lambda x: x[:10])
        
        self.data = data
        self.data_downloaded = True
    


    def export(self):
        """
        drop_cols, list of strings: columns you may want to drop
        """
        if self.data_downloaded == False:
            raise Exception("ERROR: You must first download data by calling the .download() method")
        else:
            return self.data.reset_index(drop=True)
