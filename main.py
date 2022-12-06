import keyboard
from requests import get as urlget
import os
import tkinter
from tkinter import *
from PIL import Image, ImageTk
import dotenv
import tempfile
import base64
import praw
import time
from random import randint


#Load dotenv file
dotenv.load_dotenv(dotenv.find_dotenv())

#Base64 Encoder
def encode_message(message):
    original_message = message
    message_bytes = original_message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    return base64_message
#Base64 Decoder
def decode_message(message):
    base64_message = message
    base64_bytes = base64_message.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    original_message = message_bytes.decode('ascii')
    return original_message


def enable_reddit():
    global reddit
    
    if os.getenv("base64") == 'True':
        
        reddit = praw.Reddit(
        client_id = str(decode_message(os.getenv("client_id"))),
        client_secret = str(decode_message(os.getenv("client_secret"))),
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

    else:

        reddit = praw.Reddit(
        client_id = str(os.getenv("client_id")),
        client_secret = str(os.getenv("client_secret")),
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
    top = loaded_subreddit.top(limit=500)
    
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



#Create transparent icon for Tk window, from here :D https://stackoverflow.com/questions/550050/removing-the-tk-icon-on-a-tkinter-window
def get_icon():

    
    ICON = (b'\x00\x00\x01\x00\x01\x00\x10\x10\x00\x00\x01\x00\x08\x00h\x05\x00\x00'
            b'\x16\x00\x00\x00(\x00\x00\x00\x10\x00\x00\x00 \x00\x00\x00\x01\x00'
            b'\x08\x00\x00\x00\x00\x00@\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            b'\x00\x01\x00\x00\x00\x01') + b'\x00'*1282 + b'\xff'*64

    _, ICON_PATH = tempfile.mkstemp()
    with open(ICON_PATH, 'wb') as icon_file:
        icon_file.write(ICON)
    
    return ICON_PATH

#Save loaded image to data folder
def save_image():
    
    link = get_image()
    
    r = urlget(link)

    with open('data/currentpic.jpg',"wb") as f:
        f.write(r.content)
    
#Reduce image resolution (Has to be optimized smh)
def make_good_res():

    image = Image.open('data/currentpic.jpg')

    width, height = image.size
    #print(width, height)

    while width > 700 or height > 700:
        width = round(width * 0.8)
        height = round(height * 0.8)
    
    #print(width, height)

    resized_res = width, height

    resized = image.resize(resized_res, Image.Resampling.LANCZOS)

    return resized, resized_res

#Display image in window
def display_window(good_img, good_res):

    #Create window
    window = Tk()

    #Load icon (currently transparent until I make one lmao)
    icon = get_icon()
    window.iconbitmap(default=icon)
    
    #Set window resolution and other aspects
    window.title("Kat!")
    window.configure(width=good_res[0], height=good_res[1])
    window.configure(bg='lightgray')
    window.resizable(False, False)

    #Create image object and place it in window
    image = ImageTk.PhotoImage(good_img)
    imagelabel = tkinter.Label(image=image)
    imagelabel.image = image
    imagelabel.place(x=0, y=0)

    #Destroy window after 3 seconds
    window.after(3000,lambda:window.destroy())
    
    window.mainloop()

#Run window 
def run():

    #Load and make image correct res (This needs to be moved after downloading next image to reduce loading time.)
    image, good_res = make_good_res()

    #Displays window with previously loaded image and resolution
    display_window(image, good_res)
    
    #Saves another image for next run
    save_image()



subreddit = os.getenv("subreddit")

cache_file = 'data/'+subreddit+'.txt'


if not os.path.isdir('data'):
    os.mkdir('data')


#Saves image on startup
save_image()

#Bind keychord in .env to window function
keyboard.add_hotkey(os.getenv("pic_hotkey"), run)

#Bind keychord to stop program
keyboard.wait(os.getenv("stop_hotkey"))
