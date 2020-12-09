
        ____           __    ___ __     ____        __           _____                                
       / __ \___  ____/ /___/ (_) /_   / __ \____ _/ /_____ _   / ___/______________ _____  ___  _____
      / /_/ / _ \/ __  / __  / / __/  / / / / __ `/ __/ __ `/   \__ \/ ___/ ___/ __ `/ __ \/ _ \/ ___/
     / _, _/  __/ /_/ / /_/ / / /_   / /_/ / /_/ / /_/ /_/ /   ___/ / /__/ /  / /_/ / /_/ /  __/ /    
    /_/ |_|\___/\__,_/\__,_/_/\__/  /_____/\__,_/\__/\__,_/   /____/\___/_/   \__,_/ .___/\___/_/     
                                                                              /_/                 



# RDS
Reddit Data Scraper [RDS]: A program to scrape historical data from reddit. For use in jupyter notebooks. *Quick note: I will need to refactor the code at some point, it's not as good as it could be ATM*

### Quickstart

*Step 1:* Get reddit credentials/api key, if using old reddit can be found under preferences -> apps

*Step 2:* Clone repository into working directory, either with git or by downloading the zip

*Step 3:* move into RDS repository in command line and run pip install -r requirements.txt

*Step 4*: refer to the following jupyter notebook tutorial (included in repository)


### Description

The required inputs to generate a dataset are:
- subreddit, string
- date start, tuple (Year, Month, Day)
- date end, tuple (Year, Month, Day)


The fields of data for each post currently included in a generated dataset are:

- Post date
- Post ID
- Subreddit
- Author
- Flair
- Title
- Post Text
- Score
- Upvotes
- Downvotes
- Controversiality
- Comments
- URL

### Dependencies

        praw
        psaw
        pandas
        numpy
        tqdm
        os (default)
        datetime (default)
        IPython (you will have if you are using jupyter notebooks)

### Notes
*Controversiality*: The controversiality figure is a simple function that maps the upvote ratio onto a controversiality scale between 0 and 1. It is assumed that upvote ratio values near 0, and near 1, are less controversial because they are either unanimously liked or unanimously disliked. Upvote ratio values near 0.5 would be more controversial, as there is no true agreement as to whether the post in question is worthy of upvotes or downvotes. As such, the function is graphically represented as follows:

![](images/controversial_metric_func.png)


### TODO

- Add command line program functionality
- Investigate score/upvote metric stuff
- Add ability to scrape comments
- refactor and remove redundant code
