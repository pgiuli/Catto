from cgitb import enable
import praw
import os
from random import randint
import time
import dotenv

os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
dotenv.load_dotenv(dotenv.find_dotenv())

subreddit = os.getenv("subreddit")

cache_file = 'data/'+subreddit+'.txt'


if not os.path.isdir('data'):
    os.mkdir('data')



def enable_reddit():
    global reddit
    
    reddit = praw.Reddit(
    client_id = os.getenv("client_id"),
    client_secret = os.getenv("client_secret"),
    username = os.getenv("reddit_username"),
    password = os.getenv("password"),
    user_agent = os.getenv("user_agent"),
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


def check_cached():
    
    if  os.path.exists(cache_file):

        if (os.path.getmtime(cache_file)+ 3600*48 < float(time.time())):
            os.remove(cache_file)
            return False
        else:
            return True
    else:
        return False







def get_sumbissions():
    
    enable_reddit()

    loaded_subreddit = reddit.subreddit(str(subreddit))
    top = loaded_subreddit.hot(limit=500)
    
    return top


def get_top_links():

    submissions = get_sumbissions()

    links = []

    for submission in submissions:
        link = get_link(submission)
        if check_valid_image(link):
            links.append(link)

    return links



def save_cache():

    if  os.path.exists(cache_file):
        os.remove(cache_file) 


    links = get_top_links()

    with open(cache_file, 'w') as listfile:
        for link in links:
            #print(link)
            listfile.write('%s\n' % link)


def load_cache():

    links = []
    with open(cache_file, 'r') as listfile:
            for link in listfile:
                current_link = link[:-1]
                links.append(current_link)

    return links



def get_link(submission):
    image_url = submission.url
    #print(image_url)
    return image_url


def check_valid_image(image_url):
    if 'i.redd' in image_url or 'i.imgur' in image_url:
        if image_url[-4:] == '.jpg':
            #print('valid img!')
            return True
        else:
          #print('invalid img!')
          return False


def get_image():

    if check_cached():
        links = load_cache()
    else:
        save_cache()
        links = load_cache()
        
    what_link = randint(1,len(links)-1)
    link = links[what_link]
    return link


image = get_image()

#print(image)

