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


class DynamicLabel(tk.Label):
    def __init__(self, *args, **kwargs):
        tk.Label.__init__(self, *args, **kwargs)

        # clone the font, so we can dynamically change
        # it to fit the label width
        font = self.cget("font")
        base_font = tk.font.nametofont(self.cget("font"))
        self.font = tk.font.Font()
        self.font.configure(**base_font.configure())
        self.configure(font=self.font)

        self.bind("<Configure>", self._on_configure)

    def _on_configure(self, event):
        text = self.cget("text")

        # first, grow the font until the text is too big,
        size = self.font.actual("size")
        while size < event.width:
            size += 1
            self.font.configure(size=size)

        # ... then shrink it until it fits
        while size > 1 and self.font.measure(text) > event.width:
            size -= 1
            self.font.configure(size=size)


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
    #
    # def resize(self, event):
    #     text = self.time_label.cget("text")
    #     size = self.font.actual("size")
    #     while size < event.width - 5:
    #         size += 1
    #         self.font.configure(size=size)
    #
    #     # ... then shrink it until it fits
    #     while size > 1 and self.font.measure(text) > event.width:
    #         size -= 1
    #         self.font.configure(size=size)


class Weather:
    def __init__(self, parent, address, anchor="w", side="left"):
        self.frame = tk.Frame(parent, bg="black", borderwidth=1)
        self.frame.pack(expand=True, fill="both", side=side, anchor=anchor)

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



        self.weather_description = ""
        self.weather_id = ""
        self.weather_temp_current = ""
        self.address = address

        self.frame.after(0, self.getWeatherData)

    def getWeatherData(self):
        print("GetWeatherRun")
        with urllib.request.urlopen(self.address) as url:
            data = json.loads(url.read().decode())
            weather_description = data["weather"][0]["description"]
            weather_id = data["weather"][0]["id"]
            weather_temp_current = data["main"]["temp"]

            self.current_weather_label.config(text=weather_description)
            self.current_weather_temp_label.config(text=str(round((weather_temp_current*2)/2)) + "°C")

            # Find right image for weather id
            if weather_id > 803:
                img_path = "assets/cloudy.png"
            elif weather_id > 802:
                img_path = "assets/cloudy_mostly.png"
            elif weather_id > 801:
                img_path = "assets/cloudy_partly.png"
            elif weather_id > 801:
                img_path = "assets/sunny_mostly.png"
            elif weather_id > 781:
                img_path = "assets/sunny.png"
            elif weather_id > 622:
                img_path = "assets/cloudy.png"
            elif weather_id > 602:
                img_path = "assets/sleet.png"
            elif weather_id > 601:
                img_path = "assets/snow_heavy.png"
            elif weather_id > 600:
                img_path = "assets/snow_medium.png"
            elif weather_id > 531:
                img_path = "assets/snow_light.png"
            elif weather_id > 511:
                img_path = "assets/rain_medium.png"
            elif weather_id > 504:
                img_path = "assets/sleet.png"
            elif weather_id > 501:
                img_path = "assets/rain_heavy.png"
            elif weather_id > 500:
                img_path = "assets/rain_medium.png"
            elif weather_id > 231:
                img_path = "assets/rain_light.png"
            elif weather_id >= 200:
                img_path = "assets/thunder.png"
            else:
                img_path = "assets/cloudy.png"

            self.current_weather_image = ImageTk.PhotoImage(PIL.Image.open(img_path))
            x = self.current_weather_canvas.winfo_width() / 2
            y = self.current_weather_canvas.winfo_height() / 2

            self.current_weather_canvas.itemconfig(self.image_holder, image=self.current_weather_image)
            #self.current_weather_canvas.create_image(75, 75, anchor="center", image=self.current_weather_image) delete this


        self.frame.after(3600000, self.getWeatherData)



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
        img = img.resize((150, 150), PIL.Image.ANTIALIAS)  # The (250, 250) is (height, width)
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
        self.weather = Weather(self.leftFrame,
                               "http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&APPID={}&units=metric".format(
                                   geolocation[0], geolocation[1], WEATHER_APIKEY), "e", "right")
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
