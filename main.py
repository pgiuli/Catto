import keyboard
from requests import get as urlget
import os
import tkinter
from tkinter import *
from PIL import Image, ImageTk
import dotenv
import tempfile

#Import file to download reddit images for specified subreddit
import subrredit_pics



#Load dotenv file
dotenv.load_dotenv(dotenv.find_dotenv())


def get_icon():

    #Create transparent icon for Tk window, from here :D https://stackoverflow.com/questions/550050/removing-the-tk-icon-on-a-tkinter-window

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
    
    link = subrredit_pics.get_image()
    
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


#Saves image on startup
save_image()

#Bind keychord in .env to window function
keyboard.add_hotkey(os.getenv("pic_hotkey"), run)

#Bind keychord to stop program
keyboard.wait(os.getenv("stop_hotkey"))
