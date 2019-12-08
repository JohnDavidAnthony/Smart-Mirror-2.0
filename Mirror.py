import base64
import io
import tkinter as tk
from tkinter import font
from time import strftime
import geocoder
import json
import urllib.request
from PIL import ImageTk, Image, ImageOps
import PIL.Image

import spotipy
import spotipy.util as util

from utilities import *
from Widgets import *




class FullScreen:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("500x1000")  # Width x Height
        self.window.configure(bg="black")
        self.window.attributes("-fullscreen", True)
        self.fullscreen = True
        self.window.bind('<Escape>', self.toggle_fullscreen)

        # Get Current longitude and latitude
        geolocation = geocoder.ip("me").latlng


#         Set up where the components will go
        # Top
        self.topFrame = tk.Frame(self.window, bg="black",borderwidth = 1)
        self.topFrame.grid(row=0, column=0, columnspan=3, sticky="new")
        # Bottom
        self.bottomFrame = tk.Frame(self.window, bg="black", borderwidth=1)
        self.bottomFrame.grid(row=2, column=0, columnspan=3, sticky="wes")

        # Left
        self.leftFrame = tk.Frame(self.window, bg="black", borderwidth=1)
        self.leftFrame.grid(row=1, rowspan=1, column=0, sticky="nsw")
        # Right
        self.rightFrame = tk.Frame(self.window, bg="black", borderwidth=1)
        self.rightFrame.grid(row=1, rowspan=1, column=2, sticky="nse")



        # Center
        self.centerFrame = tk.Frame(self.window, bg="black", borderwidth=1)
        self.centerFrame.grid(row=1, column=1, sticky="nsew")

        #self.window.columnconfigure(0, weight=1)
        self.window.columnconfigure(1, weight=1)
        #self.window.columnconfigure(2, weight=1)
        # # self.window.columnconfigure(3, weight=1)
        # # self.window.columnconfigure(4, weight=1)
        # self.window.columnconfigure(5, weight=1)
        # self.window.rowconfigure(0, weight=1)
        self.window.rowconfigure(1, weight=1)
        # # self.window.rowconfigure(2, weight=1)
        # # self.window.rowconfigure(3, weight=1)
        # # self.window.rowconfigure(4, weight=1)
        # self.window.rowconfigure(5, weight=1)


#         Configure Frames and add components
        # Clock
        self.clock = Clock(self.bottomFrame)
        # self.clock = Clock(self.rightFrame)
        #self.clock1 = Clock(self.topFrame)
        # self.clock = Clock(self.leftFrame)


        # Weather
        self.weather = Weather(self.leftFrame, geolocation, "e", "right")
        self.spotify = Spot(self.rightFrame, "n", "top")
        self.stauffer = Stauffer(self.rightFrame)


    def toggle_fullscreen(self, event):
        self.fullscreen = not self.fullscreen
        self.window.attributes("-fullscreen", self.fullscreen)

if __name__ == "__main__":

    screen = FullScreen()
    screen.window.mainloop()
