import keyboard
from requests import get as urlget
import os
import tkinter
from tkinter import *
from PIL import Image, ImageTk
import dotenv
import tempfile
import images
import b64converter
from random import randint


#Load dotenv file
dotenv.load_dotenv(dotenv.find_dotenv())

subreddit = os.getenv("subreddit")
sort_type = 'hot'

if os.getenv("base64") == 'True':

    client_id = b64converter.decode_message(os.getenv("client_id"))
    client_secret = b64converter.decode_message(os.getenv("client_secret"))

else:    

    client_id = os.getenv("client_id")
    client_secret = os.getenv("client_secret")

#print(client_id)
#print(client_secret)


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


#Downloads an image from the url list, saves it to a temp file, changes its resolution to fit the screen and returns a path with the new one.
def get_image():

    #Download image from one url and save it to temporary file
    url = image_urls[randint(1, len(image_urls) - 1)]
    #print('Selected url from list')

    image_data = urlget(url)

    _, badres_path = tempfile.mkstemp(suffix = '.jpg')

    with open(badres_path,"wb") as f:
        f.write(image_data.content)

    #print('Downloaded image')
    #print(badres_path)

    #Make image smaller resolution
    image = Image.open(badres_path)

    previous_width, previous_height = image.size
    ##print(width, height)


    #THIS NEEDS TO BE OPTIMIZED I HATE HOW IT WORKS
    while previous_width > 700 or previous_height > 700:
        previous_width = round(previous_width * 0.8)
        previous_height = round(previous_height * 0.8)
    
    ##print(width, height)

    good_res = previous_width, previous_height

    resized_image = image.resize(good_res, Image.Resampling.LANCZOS)

    #print('Resized image')

    return resized_image, good_res






#Display image in window
def display_window(good_img, good_res):

    #Create window
    window = Tk()

    #Load icon (currently transparent until I make one lmao)
    icon = get_icon()
    window.iconbitmap(default=icon)
    
    #Set window resolution and other aspects
    window.title("Catto")
    window.configure(width=good_res[0], height=good_res[1])
    window.configure(bg='lightgray')
    window.resizable(False, False)

    #Create image object and place it in window
    image = ImageTk.PhotoImage(good_img)
    imagelabel = tkinter.Label(image=image)
    imagelabel.image = image
    imagelabel.place(x=0, y=0)


    #Destroy window after 2.5 seconds
    window.after(2500,lambda:window.destroy())


    window.mainloop()


image_urls = images.get_urls(subreddit, sort_type, client_id, client_secret)
#print('Got URLs to main')
#print('Url list lengh: {}'.format(len(image_urls)))






#Run window 
def run():

    #Saves and resizes image
    image, good_res = get_image()

    #Displays window with previously loaded image and resolution
    display_window(image, good_res)
    




#Bind keychord in .env to window function
keyboard.add_hotkey(os.getenv("pic_hotkey"), run)

#Bind keychord to stop program
keyboard.wait(os.getenv("stop_hotkey"))








