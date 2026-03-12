"""
Weather Application - Oasis Infobyte Internship Project
Author: Ponagani Harshini
GitHub Repo: OIBSIP
Task: 2 - Weather App
Description: A beautiful weather application that fetches real-time
             weather data for any city using OpenWeatherMap API
"""

import tkinter as tk
from tkinter import messagebox
import requests
import datetime

#  API Configuration
API_KEY = "38effa6c883d8b4f0e5371ebad2fa3a4"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"

#  Weather Data Fetcher
def get_weather(city):
    try:
        params = {
            "q": city,
            "appid": API_KEY,
            "units": "metric"
        }
        response = requests.get(BASE_URL, params=params, timeout=10)
        data = response.json()

        if response.status_code == 200:
            return {
                "city": data["name"],
                "country": data["sys"]["country"],
                "temp": round(data["main"]["temp"]),
                "feels_like": round(data["main"]["feels_like"]),
                "humidity": data["main"]["humidity"],
                "pressure": data["main"]["pressure"],
                "description": data["weather"][0]["description"].title(),
                "wind_speed": data["wind"]["speed"],
                "visibility": data.get("visibility", 0) // 1000,
                "sunrise": datetime.datetime.fromtimestamp(
                    data["sys"]["sunrise"]).strftime("%I:%M %p"),
                "sunset": datetime.datetime.fromtimestamp(
                    data["sys"]["sunset"]).strftime("%I:%M %p"),
                "weather_id": data["weather"][0]["id"]
            }
        elif response.status_code == 404:
            return {"error": "City not found! Please check the city name."}
        else:
            return {"error": "Could not fetch weather. Try again!"}

    except requests.exceptions.ConnectionError:
        return {"error": "No internet connection!"}
    except Exception as e:
        return {"error": f"Something went wrong: {str(e)}"}


def get_weather_emoji(weather_id):
    if weather_id < 300:
        return "⛈️"
    elif weather_id < 400:
        return "🌧️"
    elif weather_id < 600:
        return "🌧️"
    elif weather_id < 700:
        return "❄️"
    elif weather_id < 800:
        return "🌫️"
    elif weather_id == 800:
        return "☀️"
    elif weather_id < 803:
        return "⛅"
    else:
        return "☁️"


def get_bg_color(weather_id):
    if weather_id == 800:
        return "#1a73e8", "#0d47a1"  # Sunny - bright blue
    elif weather_id < 800:
        return "#546e7a", "#263238"  # Cloudy/rainy - grey
    else:
        return "#42a5f5", "#1565c0"  # Partly cloudy

#  GUI Application
class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather App - Oasis Infobyte")
        self.root.geometry("480x700")
        self.root.configure(bg="#0f0f1a")
        self.root.resizable(False, False)

        self.unit = tk.StringVar(value="metric")
        self.build_ui()

    def build_ui(self):
        # ── Header ──
        header = tk.Frame(self.root, bg="#1a73e8", pady=15)
        header.pack(fill="x")
        tk.Label(header, text="🌦️  Weather App",
                 font=("Helvetica", 22, "bold"),
                 bg="#1a73e8", fg="white").pack()
        tk.Label(header, text="by Ponagani Harshini | Oasis Infobyte",
                 font=("Helvetica", 9), bg="#1a73e8", fg="#ddd").pack()

        # ── Search Frame ──
        search_frame = tk.Frame(self.root, bg="#0f0f1a", padx=20, pady=15)
        search_frame.pack(fill="x")

        tk.Label(search_frame, text="Enter City Name:",
                 font=("Helvetica", 11), bg="#0f0f1a", fg="#aaa").pack(anchor="w")

        input_row = tk.Frame(search_frame, bg="#0f0f1a")
        input_row.pack(fill="x", pady=5)

        self.city_entry = tk.Entry(input_row, font=("Helvetica", 13),
                                   bg="#1a1a2e", fg="white",
                                   insertbackground="white",
                                   relief="flat", bd=8)
        self.city_entry.pack(side="left", fill="x", expand=True, ipady=6)
        self.city_entry.bind("<Return>", lambda e: self.fetch_weather())
        self.city_entry.insert(0, "Hyderabad")

        tk.Button(input_row, text="Search 🔍",
                  font=("Helvetica", 11, "bold"),
                  bg="#1a73e8", fg="white", relief="flat",
                  padx=12, cursor="hand2",
                  command=self.fetch_weather).pack(side="left", padx=(8, 0))

        # ── Unit Toggle ──
        unit_frame = tk.Frame(search_frame, bg="#0f0f1a")
        unit_frame.pack(fill="x", pady=5)
        tk.Radiobutton(unit_frame, text="°C Celsius",
                       variable=self.unit, value="metric",
                       bg="#0f0f1a", fg="white",
                       selectcolor="#1a73e8",
                       activebackground="#0f0f1a",
                       command=self.fetch_weather).pack(side="left", padx=5)
        tk.Radiobutton(unit_frame, text="°F Fahrenheit",
                       variable=self.unit, value="imperial",
                       bg="#0f0f1a", fg="white",
                       selectcolor="#1a73e8",
                       activebackground="#0f0f1a",
                       command=self.fetch_weather).pack(side="left", padx=5)

        # ── Weather Display ──
        self.weather_frame = tk.Frame(self.root, bg="#1a1a2e",
                                      padx=20, pady=20,
                                      relief="ridge", bd=2)
        self.weather_frame.pack(fill="x", padx=20, pady=5)

        # City and emoji
        top_row = tk.Frame(self.weather_frame, bg="#1a1a2e")
        top_row.pack(fill="x")

        self.emoji_label = tk.Label(top_row, text="🌦️",
                                    font=("Helvetica", 48),
                                    bg="#1a1a2e", fg="white")
        self.emoji_label.pack(side="left")

        city_col = tk.Frame(top_row, bg="#1a1a2e")
        city_col.pack(side="left", padx=15)

        self.city_label = tk.Label(city_col, text="--",
                                   font=("Helvetica", 20, "bold"),
                                   bg="#1a1a2e", fg="white")
        self.city_label.pack(anchor="w")

        self.desc_label = tk.Label(city_col, text="--",
                                   font=("Helvetica", 12),
                                   bg="#1a1a2e", fg="#aaa")
        self.desc_label.pack(anchor="w")

        self.date_label = tk.Label(city_col, text="--",
                                   font=("Helvetica", 10),
                                   bg="#1a1a2e", fg="#666")
        self.date_label.pack(anchor="w")

        # Temperature
        self.temp_label = tk.Label(self.weather_frame, text="--°",
                                   font=("Helvetica", 56, "bold"),
                                   bg="#1a1a2e", fg="#1a73e8")
        self.temp_label.pack()

        self.feels_label = tk.Label(self.weather_frame, text="Feels like: --°",
                                    font=("Helvetica", 11),
                                    bg="#1a1a2e", fg="#aaa")
        self.feels_label.pack()

        # ── Details Grid ──
        details_frame = tk.Frame(self.root, bg="#0f0f1a", padx=20)
        details_frame.pack(fill="x", pady=10)

        # Row 1
        row1 = tk.Frame(details_frame, bg="#0f0f1a")
        row1.pack(fill="x", pady=3)
        self.humidity_card = self.make_card(row1, "💧 Humidity", "--")
        self.wind_card = self.make_card(row1, "💨 Wind Speed", "--")

        # Row 2
        row2 = tk.Frame(details_frame, bg="#0f0f1a")
        row2.pack(fill="x", pady=3)
        self.pressure_card = self.make_card(row2, "🔵 Pressure", "--")
        self.visibility_card = self.make_card(row2, "👁️ Visibility", "--")

        # Row 3
        row3 = tk.Frame(details_frame, bg="#0f0f1a")
        row3.pack(fill="x", pady=3)
        self.sunrise_card = self.make_card(row3, "🌅 Sunrise", "--")
        self.sunset_card = self.make_card(row3, "🌇 Sunset", "--")

        # ── Popular Cities ──
        cities_frame = tk.Frame(self.root, bg="#0f0f1a", padx=20)
        cities_frame.pack(fill="x", pady=5)
        tk.Label(cities_frame, text="Quick Search:",
                 font=("Helvetica", 9), bg="#0f0f1a", fg="#555").pack(anchor="w")
        btn_row = tk.Frame(cities_frame, bg="#0f0f1a")
        btn_row.pack(fill="x")
        for city in ["Hyderabad", "Mumbai", "Delhi", "Chennai"]:
            tk.Button(btn_row, text=city, font=("Helvetica", 9),
                      bg="#1a1a2e", fg="white", relief="flat",
                      padx=8, pady=4, cursor="hand2",
                      command=lambda c=city: self.quick_search(c)).pack(
                          side="left", padx=3)

        # Auto load
        self.fetch_weather()

    def make_card(self, parent, title, value):
        card = tk.Frame(parent, bg="#1a1a2e", padx=12, pady=8,
                        relief="flat", bd=0)
        card.pack(side="left", expand=True, fill="x", padx=3)
        tk.Label(card, text=title, font=("Helvetica", 9),
                 bg="#1a1a2e", fg="#666").pack(anchor="w")
        val_label = tk.Label(card, text=value,
                             font=("Helvetica", 13, "bold"),
                             bg="#1a1a2e", fg="white")
        val_label.pack(anchor="w")
        return val_label

    def quick_search(self, city):
        self.city_entry.delete(0, tk.END)
        self.city_entry.insert(0, city)
        self.fetch_weather()

    def fetch_weather(self):
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Input Error", "Please enter a city name!")
            return

        unit = self.unit.get()
        unit_symbol = "°C" if unit == "metric" else "°F"
        speed_unit = "m/s" if unit == "metric" else "mph"

        # Fetch with selected unit
        try:
            params = {
                "q": city,
                "appid": API_KEY,
                "units": unit
            }
            response = requests.get(BASE_URL, params=params, timeout=10)
            data = response.json()

            if response.status_code == 200:
                weather_id = data["weather"][0]["id"]
                emoji = get_weather_emoji(weather_id)
                today = datetime.datetime.now().strftime("%A, %d %B %Y")

                self.emoji_label.config(text=emoji)
                self.city_label.config(
                    text=f"{data['name']}, {data['sys']['country']}")
                self.desc_label.config(
                    text=data["weather"][0]["description"].title())
                self.date_label.config(text=today)
                self.temp_label.config(
                    text=f"{round(data['main']['temp'])}{unit_symbol}")
                self.feels_label.config(
                    text=f"Feels like: {round(data['main']['feels_like'])}{unit_symbol}")
                self.humidity_card.config(
                    text=f"{data['main']['humidity']}%")
                self.wind_card.config(
                    text=f"{data['wind']['speed']} {speed_unit}")
                self.pressure_card.config(
                    text=f"{data['main']['pressure']} hPa")
                self.visibility_card.config(
                    text=f"{data.get('visibility', 0) // 1000} km")
                self.sunrise_card.config(
                    text=datetime.datetime.fromtimestamp(
                        data["sys"]["sunrise"]).strftime("%I:%M %p"))
                self.sunset_card.config(
                    text=datetime.datetime.fromtimestamp(
                        data["sys"]["sunset"]).strftime("%I:%M %p"))

            elif response.status_code == 404:
                messagebox.showerror("Error", "City not found! Check the name.")
            else:
                messagebox.showerror("Error", "Could not fetch weather!")

        except requests.exceptions.ConnectionError:
            messagebox.showerror("Error", "No internet connection!")
        except Exception as e:
            messagebox.showerror("Error", f"Something went wrong: {str(e)}")

#  Entry Point
if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()
