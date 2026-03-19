### TASK-Voice Assistant

A Python-based Voice Assistant with a graphical interface that listens to voice commands and responds with speech and text.

## About
I built this project as part of my Python Programming Internship at Oasis Infobyte. The idea was to create a smart assistant that can understand what you say and respond helpfully.

## Features
- Responds to voice commands using microphone
- Tells current time and date
- Searches Google and YouTube
- Fetches weather information
- Answers questions using Wikipedia
- Tells jokes
- Opens websites like GitHub and LinkedIn
- Also accepts text input if microphone is unavailable

## Technologies Used
- Python 3.14
- Tkinter (GUI)
- SpeechRecognition (voice input)
- edge-tts (text to speech)
- Wikipedia API
- Requests (weather data)
- Webbrowser (open websites)

## How to Run

Install the required libraries:
```
pip install SpeechRecognition edge-tts wikipedia requests sounddevice
```

Run the project:
```
python voice_assistant.py
```

## Commands You Can Try
- "Hello" - greets you
- "What is the time?" - tells current time
- "What is today's date?" - tells the date
- "Tell me a joke" - tells a joke
- "What is Python?" - Wikipedia summary
- "Search machine learning" - opens Google
- "Weather in Hyderabad" - shows weather
- "Open YouTube" - opens YouTube
- "Goodbye" - closes the assistant

## Author
Ponagani Harshini
Oasis Infobyte Python Programming Internship


### Task 2 - Weather App

A weather app I built using Python that shows 
real-time weather details for any city you search.

### About
I built this project as part of my Python 
Programming Internship at Oasis Infobyte. The idea 
was to create a simple app where you can type any 
city name and instantly see its current weather.

### Features
- Search weather for any city
- Shows current temperature in °C or °F
- Shows feels like temperature
- Shows humidity, wind speed and pressure
- Shows visibility in km
- Shows sunrise and sunset times
- Weather emoji changes based on conditions
- Quick search buttons for Hyderabad, Mumbai, 
  Delhi and Chennai

### Technologies Used
- Python 3
- Tkinter for GUI window
- OpenWeatherMap API for weather data
- Requests to fetch data from API
- Datetime to show date and time

### How to Run
pip install requests
python weather_app.py

### Author
Ponagani Harshini
Oasis Infobyte Python Programming Internship
