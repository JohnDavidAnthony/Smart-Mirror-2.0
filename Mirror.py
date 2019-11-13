import tkinter as tk
from tkinter import font
from time import strftime
import geocoder
import json
import urllib.request


class Clock:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg="black")
        self.font = font.Font(family='Helvetica')
        self.frame.bind('<Configure>', self.resize)
        self.frame.pack(padx=30)
        self.time = None
        self.time_label = tk.Label(self.frame, font=self.font, fg="white", bg="black")
        self.time_label.pack(anchor="center", expand=True, fill="both")

        self.tick()

    def tick(self):
        time = strftime("%H:%M:%S %p")
        self.time_label.config(text=time)
        self.time_label.after(1000, self.tick)

    def resize(self, event):
        self.font.config(size=int(.18*event.width))
        print(event.width)

class Weather:
    def __init__(self, parent, address):
        self.getWeatherData(address)

    def getWeatherData(self, address):
        with urllib.request.urlopen(address) as url:
            data = json.loads(url.read().decode())
            print (data)


class FullScreen:
    def __init__(self):
        self.window = tk.Tk()
        self.window.configure(bg="black")
        #self.window.attributes("-fullscreen", True)

        # Get Current longitude and latitude
        geolocation = geocoder.ip("me").latlng


#         Set up where the components will go
        # Top
        self.topFrame = tk.Frame(self.window, bg="black")
        self.topFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=False)
        # Bottom
        self.bottomFrame = tk.Frame(self.window, bg="black")
        self.bottomFrame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=False)

#         Configure Frames and add components
        # Clock
        self.clock = Clock(self.bottomFrame)

        # Weather
        self.weather = Weather(self.topFrame, "http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&APPID={}".format(geolocation[0], geolocation[1], APIKEY))



if __name__ == "__main__":
    APIKEY = "dec6af11d23906a2380e2214c2416010"
    screen = FullScreen()
    screen.window.mainloop()
