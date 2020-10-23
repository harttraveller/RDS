
        ____           __    ___ __     ____        __           _____                                
       / __ \___  ____/ /___/ (_) /_   / __ \____ _/ /_____ _   / ___/______________ _____  ___  _____
      / /_/ / _ \/ __  / __  / / __/  / / / / __ `/ __/ __ `/   \__ \/ ___/ ___/ __ `/ __ \/ _ \/ ___/
     / _, _/  __/ /_/ / /_/ / / /_   / /_/ / /_/ / /_/ /_/ /   ___/ / /__/ /  / /_/ / /_/ /  __/ /    
    /_/ |_|\___/\__,_/\__,_/_/\__/  /_____/\__,_/\__/\__,_/   /____/\___/_/   \__,_/ .___/\___/_/     
                                                                              /_/                 



# RDS
Reddit Data Scraper [RDS]: A program to scrape historical data from reddit. *Quick note: I will need to refactor the code at some point, it's not as good as it could be ATM*


### Description

The required inputs to generate a dataset are:
- subreddit
- date range
- dataset export path/dataset export type (currently supports csv, xlsx)
- daily post limit


The fields of data for each post currently included in a generated dataset are:

- Author
- Post date
- UTC creation datetime
- Post ID
- Number of comments
- Upvotes
- Subreddit
- Post title
- Upvote ratio
- Post URL
- Downvotes
- Controversiality

### Dependencies

### Quickstart

### Notes
*Downvotes*: Because downvotes are not actually given, downvotes are calculated using the number of upvotes and the upvote ratio. Often this calculation results in a non-integer value, thus, one should not treat downvotes as exact, as they are often rounded from float values.

*Controversiality*: The controversiality figure is a simple function that maps the upvote ratio onto a controversiality scale between 0 and 1. It is assumed that upvote ratio values near 0, and near 1, are less controversial because they are either unanimously liked or unanimously disliked. Upvote ratio values near 0.5 would be more controversial, as there is no true agreement as to whether the post in question is worthy of upvotes or downvotes. As such, the function is graphically represented as follows:

![](images/controversial_metric_func.png)


### TODO

- Add command line program functionality
