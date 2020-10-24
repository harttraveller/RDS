
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
*Voting*
PRAW says that the "score" metric they return for a post is not actually the score for a post, but the number of upvotes: https://praw.readthedocs.io/en/latest/code_overview/models/submission.html.


Because we can't actually get the number of downvotes or upvotes for a post through praw or psaw, downvotes and upvotes are estimated using score and the upvote ratio. Often this calculation results in a non-integer value, thus, one should not treat downvotes/upvotes as exact, as they are often rounded from float values. Furthermore, the dysjunction between the PRAW documentation and basic reason seriously weakens my confidence in these figures, as I'm still not entirely confident whether the score metric is upvotes (what they suggest, but seemingly impossible), or the score of a post (what the parameter name suggests, makes more sense). If the score metric returned is truly the score and not the upvotes, then confusingly, they also return all scores less than 0 as 0. Furthermore, I have heard that seem to suggest that the score metric IS upvotes, because people have had their comments downvoted such that they have a negative score, but PRAW still returns a score of 1.

Finally, whether the metric is upvotes or score, it is impossible to estimate the number of downvotes if the score/upvotes metric is zero. If the metric is upvotes, but it is zero, then the downvotes would be calculated 

For our calculation, we assume this is the case, and that in fact the PRAW documentation is 


*Caveats*
You can never actually calculate the number of downvotes when the score/upvotes metric is 0, whether it refers to upvotes or literal score. Even though the documentation on PRAW suggests that it refers to upvotes, it is hard to tell because this is logically inconsistent with a upvote metric of 0, and a non zero upvote ratio, which we find for many posts. This strongly suggests what is actually being recorded is the score, and that reddit opts to show you when a score is negative.



*Controversiality*: The controversiality figure is a simple function that maps the upvote ratio onto a controversiality scale between 0 and 1. It is assumed that upvote ratio values near 0, and near 1, are less controversial because they are either unanimously liked or unanimously disliked. Upvote ratio values near 0.5 would be more controversial, as there is no true agreement as to whether the post in question is worthy of upvotes or downvotes. As such, the function is graphically represented as follows:

![](images/controversial_metric_func.png)


### TODO

- Add command line program functionality
- Investigate score/upvote metric stuff
- Add ability to scrape comments
