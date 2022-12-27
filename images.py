import praw

#Creates reddit instance using praw
def enable_reddit(client_id, client_secret):

    reddit_instance = praw.Reddit(
    client_id = str(client_id),
    client_secret = str(client_secret),
    user_agent = 'Catto',
    check_for_updates=False,
    comment_kind="t1",
    message_kind="t4",
    redditor_kind="t2",
    submission_kind="t3",
    subreddit_kind="t5",
    trophy_kind="t6",
    oauth_url="https://oauth.reddit.com",
    reddit_url="https://www.reddit.com",
    short_url="https://redd.it",
    ratelimit_seconds=5,
    timeout=16,
    )

    return reddit_instance


#Method to check if image link is valid. Returns True or False

def check_valid_image(image_url):
    if 'i.redd' in image_url or 'i.imgur' in image_url:
        if image_url[-4:] == '.jpg' or image_url[-4:] == '.png':
            #print('valid img!')
            return True
        else:
            #print('invalid img!')
            return False
    else:
            #print('invalid img!')
            return False

#Method to get .jpg and .png urls for posts in subreddit. Returns an array
def extract_image_urls(subreddit, sort_type, reddit_instance):
    #Load subreddit object
    loaded_subreddit = reddit_instance.subreddit(str(subreddit))
    #print('Loaded subreddit')

    #Get submission IDs from praw 
    if str(sort_type) == 'hot':
        submission_ids = loaded_subreddit.hot(limit=50)
    else:
        submission_ids = loaded_subreddit.top(limit=50)

    #print('Gotten submission IDs')

    #Get image urls from ids
    urls = []

    for id in submission_ids:
        url = id.url
        if check_valid_image(url):
            urls.append(url)
    
    #print('Appended URLs')

    return urls
    



def get_urls(subreddit, sort_type, client_id, client_secret):

    reddit_instance = enable_reddit(client_id, client_secret)
    #print('Created reddit instance')

    urls = extract_image_urls(subreddit, sort_type, reddit_instance)
    #print('Finished extracting urls')

    return urls



