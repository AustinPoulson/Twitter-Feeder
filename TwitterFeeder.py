import praw
import twitter
import time

#global variables
#This is the minimum amount of upvotes a Reddit post needs to have in order to be selected for the twitter feed.
minScore = 150

while True:
   try: #to connect to reddit and twitter
      #connect to reddit
      reddit = praw.Reddit(client_id='[client ID]',
                     client_secret='[client secret]',
                     username='[username]',
                     password='[password]',
                     user_agent='[user agent]')
                     
      #connect to twitter
      api = twitter.Api(consumer_key='[consumer key]',
              consumer_secret='[consumer secret]',
              access_token_key='[access token key]',
              access_token_secret='[access token secret]')
   except: #if the connection fails, tell the user and continue.
      print('Could not connect to one or more APIs')
      
   try: #to define the content sources.
      #define subreddits to use as content sources
      readsubreddit = reddit.subreddit('[one or more subreddits, seperated by plus signs]')
   except: #if the content sources can't be defined, tell the user and delay for 30 seconds.
      print('Could not connect to one or more subreddits')
      time.sleep(30)

   rejectCounter = 0 #This variable helps to keep the script looping.
   
   #This is the main loop of the script. 
   for submission in readsubreddit.stream.submissions():
      try: #to find submissions and filter them. If a post passes filtering, find which type of post it is, and post its content to twitter using the correct posting method.
         if submission.score > minScore: #find the posts that have gained more than the specified number of upvotes.
            if submission.is_self == True: #Post the title of a text post.
               print('Posting self post.')
               tweet = api.PostUpdate(submission.title)
               print('Self post successful.')
               rejectCounter = 0
               print('Sleeping for 1 hour.')
               time.sleep(3600)
            else: #Post the picture from an image post.
               print('Posting image post.')
               tweet = api.PostUpdate('', media=submission.url)
               print('Image post successful.')
               rejectCounter = 0
               print('Sleeping for 1 hour.')
               time.sleep(3600)
         else: #reject posts that don't have enough upvotes and add one to the reject counter.
            rejectCounter += 1
            print('post rejected: #'+str(rejectCounter))
            if rejectCounter >= 100: #If the reject counter hits 100 posts, then the script has caught up with the all the posts. This means that new posts being read will never have more than one upvote. 
               print('Refreshing')
               break #Once the limit is met. This will break the current loop, and the outer 'while' loop will reinitiate the program.
      except Exception as e: #if something goes wrong with the post, the issue will be caught here. This is usually a connection issue.
         print('Post unsuccessful')
         print(e)
         time.sleep(30) #This line will allow time for temporary connection failures to pass.
