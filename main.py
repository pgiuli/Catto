import keyboard
from requests import get as urlget
import os
import tkinter
from tkinter import *
from PIL import Image, ImageTk
import dotenv
from time import sleep

import subrredit_pics



dotenv.load_dotenv(dotenv.find_dotenv())


def save_image():
    
    link = subrredit_pics.get_image()
    

    r = urlget(link)
    
    with open('data/currentpic.jpg',"wb") as f:
        f.write(r.content)
    



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


def display_window(good_img, good_res):


    good_width, good_height = good_res

    window = Tk()

    window.title("Sporko Catto!!!")
    window.configure(width=good_width, height=good_height)
    window.configure(bg='lightgray')
    window.resizable(False, False)


    image = ImageTk.PhotoImage(good_img)

    label1 = tkinter.Label(image=image)
    label1.image = image


    label1.place(x=0, y=0)

    window.after(3000,lambda:window.destroy())
    
    
    window.mainloop()



def run():

    image, good_res = make_good_res()

    display_window(image, good_res)

    save_image()

save_image()


keyboard.add_hotkey(os.getenv("cat_hotkey"), run)


keyboard.wait(os.getenv("stop_hotkey"))
