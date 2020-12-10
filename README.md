
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
        sympy
        pandas
        numpy
        tqdm
        os (default)
        datetime (default)
        IPython (you will have if you are using jupyter notebooks)

### Notes
*Solving for upvotes and downvotes*: Praw does not actually tell you how many upvotes or downvotes a post has. It simply gives you the score (upvotes minus downvotes), and the upvote ratio (praw docs quote this as: "The percentage of upvotes from all votes on the submission")

Using this information, we can derive a system of linear equations that allows us to solve for the number of upvotes and downvotes however.
```
score = upvotes - downvotes
upvotes = score + downvotes
upvotes - downvotes - score = 0

upvote_ratio = upvotes/(upvotes+downvotes)
upvote_ratio*(upvotes+downvotes) = upvotes
upvotes_ratio*(upvotes+downvotes) - upvotes = 0
```
We can then simply plug the system of linear equations into sympy to solve for the number of upvotes and downvotes.

One problem with this, is that it would be logically impossible to have a post with an upvote ratio of 0.5, and a non zero score, as an upvote ratio of 0.5 means 50% of the votes on the submission were upvotes, which in turn means 50% must be downvotes. Unfortunately, it is quite common to see this logical impossibility in the data provided by reddit. This suggests that what the reddit documentation authors mean is "the percentage of upvotes from the sum of votes on the submission (or in other words the score)". If this is the case however, it would be impossible to have an upvote ratio less than 1, as the sum of the upvotes will always be greater than or equal to the sum of the upvotes plus (subtracted) downvotes. So perhaps what the reddit documentation authors mean that the upvote ratio is calculated as the score of the post divided by the number of upvotes, though this is a stretch. It does appear to work in that it permits positive scores with upvote ratios of 0.5, and subtracting the calculated downvotes from the upvotes does yield the score, but unfortunately it also manifests strange artifacts, such as upvote ratios of 0.5 corresponding to posts where there are twice as many upvotes as downvotes, which doesn't make much intuitive sense. Whether it is the reddit engineers ineptitude, or their attempts at obfuscating data, we may never know - that is unless you have an idea, in which case please contact me because I'm dying to know!

At any rate, upvotes and downvotes are assumed to be as described in the documentation, and are derived from the linear system of equations. All artifacts where a post has a positive score but an upvote ratio of 0.5 give upvote and downvote scores of 0 for both.



*Controversiality*: The controversiality figure is a simple function that maps the upvote ratio onto a controversiality scale between 0 and 1. It is assumed that upvote ratio values near 0, and near 1, are less controversial because they are either unanimously liked or unanimously disliked. Upvote ratio values near 0.5 would be more controversial, as there is no true agreement as to whether the post in question is worthy of upvotes or downvotes. As such, the function is graphically represented as follows:

![](images/controversial_metric_func.png)


### TODO

- Add command line program functionality
- Investigate score/upvote metric stuff
- Add ability to scrape comments
- refactor and remove redundant code
