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


class Clock:
    def __init__(self, parent, anchor="s", side="bottom"):
        self.time = None
        self.time_label = tk.Label(parent, font=('Helvetica', FONTSIZE), fg="white", bg="black")
        # self.time_label.bind('<Configure>', self.resize)
        self.time_label.pack(side=side, anchor=anchor, expand=False, fill="x")

        self.tick()

    def tick(self):
        time = strftime("%H:%M:%S %p")
        self.time_label.config(text=time)
        self.time_label.after(1000, self.tick)


class Weather:
    def __init__(self, parent, geo_location, anchor="w", side="left"):
        self.frame = tk.Frame(parent, bg="black", borderwidth=1)
        self.frame.pack(expand=True, fill="both", side=side, anchor=anchor)

        self.geo_location = geo_location

        # Current Weather

        self.current_weather_frame = tk.Frame(self.frame, bg="black", borderwidth=1)
        self.current_weather_frame.pack(side="top", anchor="n", fill="x", expand=True)
        # Current Weather icon
        self.current_weather_canvas = tk.Canvas(self.current_weather_frame, bg="black", width=150, height=150, highlightthickness=0)
        self.current_weather_canvas.pack(fill="x", expand=True, anchor="center", padx=50)
        self.current_weather_image = ImageTk.PhotoImage(file="assets/cloudy.png")

        self.current_weather_canvas.update()
        x = self.current_weather_canvas.winfo_width() / 2
        y = self.current_weather_canvas.winfo_height() / 2
        self.image_holder = self.current_weather_canvas.create_image(x, y, anchor="center", image=self.current_weather_image)

        self.font = font.Font(family=('Helvetica',FONTSIZE))
        # self.frame.bind('<Configure>', self.resize)

        self.current_weather_temp_label = tk.Label(self.current_weather_frame, font=('Helvetica', FONTSIZE), fg="white", bg="black")
        self.current_weather_temp_label.pack(side="top", anchor="n", expand=True, fill="x", padx=5)

        self.current_weather_label = tk.Label(self.current_weather_frame, font=('Helvetica',FONTSIZE), fg="white", bg="black")
        self.current_weather_label.pack(anchor=anchor, side=side, expand=True, fill="x", padx=5)
        self.current_weather_label.config(text="                             ")

        # Future Weather _________________

        self.future_weather_frame = tk.Frame(self.frame, bg="black", borderwidth=1)
        self.future_weather_frame.pack(side="top", anchor="n", fill="x", expand=True)

        # 3hr Weather icon
        self.hr3_frame = tk.Frame(self.future_weather_frame, bg="black", borderwidth=1)
        self.hr3_frame.pack(side="top", anchor="n", fill="x", expand=True)
        self.hr3_weather_canvas = tk.Canvas(self.hr3_frame, bg="black", width=75, height=75,
                                                highlightthickness=0)
        self.hr3_weather_canvas.grid(columnspan=3, row=1, padx=50)
        self.hr3_weather_image = ImageTk.PhotoImage(file="assets/cloudy.png")
        self.hr3_weather_canvas.update()
        x = self.hr3_weather_canvas.winfo_width() / 2
        y = self.hr3_weather_canvas.winfo_height() / 2
        self.hr3_image_holder = self.hr3_weather_canvas.create_image(x, y, anchor="center",
                                                                     image=self.hr3_weather_image)
        self.hr3_title = tk.Label(self.hr3_frame, font=('Helvetica', FONTSIZE),
                                               fg="white",
                                               bg="black", text="Later Today")
        self.hr3_title.grid(row=0, columnspan=3, padx=5)
        self.hr3_weather_temp_label = tk.Label(self.hr3_frame, font=('Helvetica', int(FONTSIZE/2)), fg="white",
                                                   bg="black")
        self.hr3_weather_temp_label.grid(row=2, column=2, padx=5)
        self.hr3_weather_label = tk.Label(self.hr3_frame, font=('Helvetica', int(FONTSIZE/2)), fg="white",
                                              bg="black")
        self.hr3_weather_label.grid(row=2, columnspan=2, padx=5)

        # 1 Day Weather __________
        self.day1_frame = tk.Frame(self.future_weather_frame, bg="black", borderwidth=1)
        self.day1_frame.pack(side="top", anchor="n", fill="x", expand=True)
        self.day1_weather_canvas = tk.Canvas(self.day1_frame, bg="black", width=75, height=75,
                                                highlightthickness=0)
        self.day1_weather_canvas.grid(columnspan=3, row=1, padx=50)
        self.day1_weather_image = ImageTk.PhotoImage(file="assets/cloudy.png")
        self.day1_weather_canvas.update()
        x = self.day1_weather_canvas.winfo_width() / 2
        y = self.day1_weather_canvas.winfo_height() / 2
        self.day1_image_holder = self.day1_weather_canvas.create_image(x, y, anchor="center",
                                                                     image=self.day1_weather_image)
        self.day1_title = tk.Label(self.day1_frame, font=('Helvetica', FONTSIZE),
                                               fg="white",
                                               bg="black", text="Tomorrow")
        self.day1_title.grid(row=0, columnspan=3, padx=5)
        self.day1_weather_temp_label = tk.Label(self.day1_frame, font=('Helvetica', int(FONTSIZE/2)), fg="white",
                                                   bg="black")
        self.day1_weather_temp_label.grid(row=2, column=2, padx=5)
        self.day1_weather_label = tk.Label(self.day1_frame, font=('Helvetica', int(FONTSIZE/2)), fg="white",
                                              bg="black")
        self.day1_weather_label.grid(row=2, columnspan=2, padx=5)

        self.weather_description = ""
        self.weather_id = ""
        self.weather_temp_current = ""

        self.frame.after(0, self.getCurrentWeather)
        self.frame.after(0, self.getFutureWeather)

    def getCurrentWeather(self):
        print("GetCurrentWeatherRun")
        address = "http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&APPID={}&units=metric".format(self.geo_location[0], self.geo_location[1], WEATHER_APIKEY)
        with urllib.request.urlopen(address) as url:
            data = json.loads(url.read().decode())
            weather_description = data["weather"][0]["description"]
            weather_id = data["weather"][0]["id"]
            weather_temp_current = data["main"]["temp"]

            self.current_weather_label.config(text=weather_description)
            self.current_weather_temp_label.config(text=str(round((weather_temp_current*2)/2)) + "°C")

            img_path = self.code_to_path(weather_id)
            self.current_weather_image = ImageTk.PhotoImage(PIL.Image.open(img_path))

            self.current_weather_canvas.itemconfig(self.image_holder, image=self.current_weather_image)

        self.frame.after(3600000, self.getCurrentWeather)

    def getFutureWeather(self):
        print("GetFutureWeatherRun")
        address = "http://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&APPID={}&units=metric".format(
            self.geo_location[0], self.geo_location[1], WEATHER_APIKEY)
        with urllib.request.urlopen(address) as url:
            data = json.loads(url.read().decode())

            hours_3 = data["list"][0]
            img_path = self.code_to_path(hours_3["weather"][0]["id"])
            image = Image.open(img_path)
            image = image.resize((75, 75), Image.ANTIALIAS)
            self.hr3_weather_image = ImageTk.PhotoImage(image)
            self.hr3_weather_canvas.itemconfig(self.hr3_image_holder, image=self.hr3_weather_image)
            self.hr3_weather_temp_label.config(text=str(round((hours_3["main"]["temp"] * 2) / 2)) + "°C")
            self.hr3_weather_label.config(text=hours_3["weather"][0]["description"])

            day_1 = data["list"][3]
            img_path = self.code_to_path(day_1["weather"][0]["id"])
            image = Image.open(img_path)
            image = image.resize((75, 75), Image.ANTIALIAS)
            self.day1_weather_image = ImageTk.PhotoImage(image)
            self.day1_weather_canvas.itemconfig(self.day1_image_holder, image=self.day1_weather_image)
            self.day1_weather_temp_label.config(text=str(round((day_1["main"]["temp"] * 2) / 2)) + "°C")
            self.day1_weather_label.config(text=day_1["weather"][0]["description"])

            day_2 = data["list"][7]
            day_3 = data["list"][11]

        self.frame.after(10800000, self.getFutureWeather)

    def code_to_path(self, code):
        # Find right image for weather id
        if code > 803:
            img_path = "assets/cloudy.png"
        elif code > 802:
            img_path = "assets/cloudy_mostly.png"
        elif code > 801:
            img_path = "assets/cloudy_partly.png"
        elif code > 801:
            img_path = "assets/sunny_mostly.png"
        elif code > 781:
            img_path = "assets/sunny.png"
        elif code > 622:
            img_path = "assets/cloudy.png"
        elif code > 602:
            img_path = "assets/sleet.png"
        elif code > 601:
            img_path = "assets/snow_heavy.png"
        elif code > 600:
            img_path = "assets/snow_medium.png"
        elif code > 531:
            img_path = "assets/snow_light.png"
        elif code > 511:
            img_path = "assets/rain_medium.png"
        elif code > 504:
            img_path = "assets/sleet.png"
        elif code > 501:
            img_path = "assets/rain_heavy.png"
        elif code > 500:
            img_path = "assets/rain_medium.png"
        elif code > 231:
            img_path = "assets/rain_light.png"
        elif code >= 200:
            img_path = "assets/thunder.png"
        else:
            img_path = "assets/cloudy.png"

        return img_path

    def resize(self, event):
        text = self.current_weather_label.cget("text")
        size = self.font.actual("size")
        while size < event.width - 5:
            size += 3
            self.font.configure(size=size)

        # ... then shrink it until it fits
        while size > 3 and self.font.measure(text) > event.width +5:
            size -= 3
            self.font.configure(size=size)


class Spot:
    def auth(self):
        scope = "user-read-currently-playing"
        token = util.prompt_for_user_token(USERNAME, scope, client_id=SPOTIPY_CLIENT_ID,
                                           client_secret=SPOTIPY_CLIENT_SECRET,
                                           redirect_uri=SPOTIPY_REDIRECT_URI)

        self.spotify = spotipy.Spotify(auth=token)

    def __init__(self, parent, anchor="e", side="right"):
        self.spotify = None

        self.auth()

        # Spotify Frame
        self.frame = tk.Frame(parent, bg="black", borderwidth=1)
        self.frame.pack(expand=True, fill="x", side=side, anchor=anchor)


        # Current song artwork

        self.current_song_canvas = tk.Canvas(self.frame, bg="black", width=150, height=150, highlightthickness=0)
        self.current_song_canvas.pack(fill="x", expand=True, padx=50)

        self.default_cover_art = "https://lh3.googleusercontent.com/UrY7BAZ-XfXGpfkeWg0zCCeo-7ras4DCoRalC_WXXWTK9q5b0Iw7B0YQMsVxZaNB7DM"
        image_byt = urllib.request.urlopen(self.default_cover_art).read()
        img = PIL.Image.open(io.BytesIO(image_byt))
        img = img.resize((150, 150), PIL.Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(img)

        self.current_song_canvas.update()
        x = self.current_song_canvas.winfo_width() / 2
        y = self.current_song_canvas.winfo_height() / 2
        self.image_holder = self.current_song_canvas.create_image(x, y, anchor="center", image=self.photo)

        #Current song Labels
        self.current_song_marquee = Marquee(self.frame, text="Nothing's Playing", relief="sunken", textbox_width=300)
        self.current_song_marquee.itemconfig(self.current_song_marquee.text_id, font=('Helvetica', FONTSIZE))
        self.current_song_marquee.pack(side="bottom", anchor="s", fill="y", pady=20, padx=5)

        # self.current_song_name_label = tk.Label(self.frame, font=('Helvetica', FONTSIZE), fg="white",
        #                                       bg="black", wraplength=300)
        # self.current_song_name_label.pack(anchor="s", side="bottom", expand=True, fill="x", padx=5, )

        self.current_song_artist_label = tk.Label(self.frame, font=('Helvetica', FONTSIZE), fg="white",bg="black")
        self.current_song_artist_label.pack(side="bottom", anchor="s", expand=True, fill="x", padx=5)

        self.getCurrentSong()

    def getCurrentSong(self):
        print("GetCurrentSongRun")
        if self.spotify is not None:
            try:
                current_track = self.spotify.current_user_playing_track()

            except:
                self.auth()
                current_track = self.spotify.current_user_playing_track()

            if current_track is None:
                song = "Nothing's Playing"
                artwork = self.default_cover_art
                artist = ""
            else:
                song = current_track["item"]["name"]
                artwork = current_track["item"]["album"]["images"][1]["url"]
                artist = current_track["item"]["artists"][0]["name"]

            image_byt = urllib.request.urlopen(artwork).read()
            img = PIL.Image.open(io.BytesIO(image_byt))
            img = img.resize((150, 150), PIL.Image.ANTIALIAS)  # The (250, 250) is (height, width)
            self.photo = ImageTk.PhotoImage(img)

            self.current_song_canvas.itemconfig(self.image_holder, image=self.photo)

            self.current_song_artist_label.config(text=artist)
            self.current_song_marquee.change_text(song)

        self.frame.after(10000, self.getCurrentSong)


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


    def toggle_fullscreen(self, event):
        self.fullscreen = not self.fullscreen
        self.window.attributes("-fullscreen", self.fullscreen)

if __name__ == "__main__":
    WEATHER_APIKEY = "dec6af11d23906a2380e2214c2416010"

    USERNAME = "12161261106"
    SPOTIPY_CLIENT_ID = "c3b0ff91599c4df9a93a0679dff547ce"
    SPOTIPY_CLIENT_SECRET = "e5196078ac304a31a5d8116762e3c69d"
    SPOTIPY_REDIRECT_URI = "http://localhost/"

    FONTSIZE = 36
    screen = FullScreen()
    screen.window.mainloop()
