"""
Voice Assistant - Oasis Infobyte Internship Project
Author: Ponagani Harshini
GitHub Repo: OIBSIP
Python 3.14 Compatible Version
"""

import tkinter as tk
from tkinter import scrolledtext
import threading
import datetime
import webbrowser
import random
import subprocess
import speech_recognition as sr
import wikipedia
import requests
import asyncio
import edge_tts
import os


# ─────────────────────────────────────────────
#  Text-to-Speech using edge-tts
# ─────────────────────────────────────────────

def speak(text):
    async def _speak():
        communicate = edge_tts.Communicate(text, voice="en-IN-NeerjaNeural")
        await communicate.save("speech.mp3")
    asyncio.run(_speak())
    os.system("start speech.mp3")


# ─────────────────────────────────────────────
#  Speech Recognition
# ─────────────────────────────────────────────

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
            command = recognizer.recognize_google(audio).lower()
            return command
        except sr.WaitTimeoutError:
            return "timeout"
        except sr.UnknownValueError:
            return "unknown"
        except sr.RequestError:
            return "error"
        except Exception:
            return "error"


# ─────────────────────────────────────────────
#  Assistant Brain
# ─────────────────────────────────────────────

JOKES = [
    "Why do programmers prefer dark mode? Because light attracts bugs!",
    "Why did the Python programmer get lost? Because they didn't know where to INDENT!",
    "I told my computer I needed a break... now it won't stop sending me Kit-Kat ads.",
    "Why do Java developers wear glasses? Because they don't C#!",
    "A SQL query walks into a bar and asks two tables... Can I join you?"
]

def process_command(command):
    if any(word in command for word in ["hello", "hi", "hey"]):
        hour = datetime.datetime.now().hour
        if hour < 12:
            return "Good morning! How can I help you today?"
        elif hour < 17:
            return "Good afternoon! What can I do for you?"
        else:
            return "Good evening! How may I assist you?"
    elif "time" in command:
        now = datetime.datetime.now().strftime("%I:%M %p")
        return f"The current time is {now}."
    elif "date" in command or "today" in command:
        today = datetime.datetime.now().strftime("%A, %d %B %Y")
        return f"Today is {today}."
    elif "day" in command:
        day = datetime.datetime.now().strftime("%A")
        return f"Today is {day}."
    elif "joke" in command:
        return random.choice(JOKES)
    elif "who is" in command or "what is" in command or "tell me about" in command:
        query = (command.replace("who is", "").replace("what is", "").replace("tell me about", "").strip())
        try:
            result = wikipedia.summary(query, sentences=2)
            return result
        except Exception:
            return f"Sorry, I couldn't find information about {query}."
    elif "search" in command or "google" in command:
        query = command.replace("search", "").replace("google", "").strip()
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        webbrowser.open(url)
        return f"Searching Google for: {query}"
    elif "youtube" in command:
        query = command.replace("youtube", "").replace("play", "").strip()
        url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
        webbrowser.open(url)
        return f"Opening YouTube for: {query}"
    elif "weather" in command:
        city = command.replace("weather", "").replace("in", "").strip()
        if not city:
            city = "Hyderabad"
        try:
            url = f"https://wttr.in/{city}?format=3"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return response.text
            else:
                return f"Could not fetch weather for {city}."
        except Exception:
            return f"Could not fetch weather. Check your internet."
    elif "open" in command:
        if "youtube" in command:
            webbrowser.open("https://youtube.com")
            return "Opening YouTube."
        elif "google" in command:
            webbrowser.open("https://google.com")
            return "Opening Google."
        elif "github" in command:
            webbrowser.open("https://github.com")
            return "Opening GitHub."
        elif "linkedin" in command:
            webbrowser.open("https://linkedin.com")
            return "Opening LinkedIn."
        else:
            return "I'm not sure which website to open."
    elif "your name" in command or "who are you" in command:
        return "I am Harshini's Voice Assistant, built with Python for Oasis Infobyte!"
    elif "who made you" in command or "who created you" in command:
        return "I was created by Ponagani Harshini for the Oasis Infobyte Internship."
    elif any(word in command for word in ["bye", "goodbye", "exit", "stop", "quit"]):
        return "Goodbye! Have a wonderful day!"
    elif "help" in command or "what can you do" in command:
        return "I can tell time and date, search Google and YouTube, tell jokes, give Wikipedia summaries, check weather, and open websites!"
    elif command == "timeout":
        return "I didn't hear anything. Please try again."
    elif command in ("unknown", "error"):
        return "Sorry, I didn't catch that. Could you repeat?"
    else:
        return f"I heard: '{command}'. Try asking about time, weather, or jokes!"


# ─────────────────────────────────────────────
#  GUI Application
# ─────────────────────────────────────────────

class VoiceAssistantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Voice Assistant - Oasis Infobyte")
        self.root.geometry("560x700")
        self.root.configure(bg="#0f0f1a")
        self.root.resizable(False, False)
        self.is_listening = False
        self.build_ui()
        self.greet()

    def build_ui(self):
        header = tk.Frame(self.root, bg="#6c63ff", pady=16)
        header.pack(fill="x")
        tk.Label(header, text="Voice Assistant", font=("Helvetica", 22, "bold"), bg="#6c63ff", fg="white").pack()
        tk.Label(header, text="by Ponagani Harshini | Oasis Infobyte", font=("Helvetica", 9), bg="#6c63ff", fg="#ddd").pack()

        self.status_frame = tk.Frame(self.root, bg="#0f0f1a")
        self.status_frame.pack(pady=10)
        self.status_dot = tk.Label(self.status_frame, text="●", font=("Helvetica", 18), bg="#0f0f1a", fg="#2ecc71")
        self.status_dot.pack(side="left", padx=5)
        self.status_label = tk.Label(self.status_frame, text="Ready", font=("Helvetica", 12), bg="#0f0f1a", fg="#2ecc71")
        self.status_label.pack(side="left")

        chat_frame = tk.Frame(self.root, bg="#0f0f1a", padx=20)
        chat_frame.pack(fill="both", expand=True)
        self.chat_box = scrolledtext.ScrolledText(chat_frame, font=("Helvetica", 11), bg="#1a1a2e", fg="white", wrap=tk.WORD, relief="flat", bd=0, padx=10, pady=10, state="disabled", height=18)
        self.chat_box.pack(fill="both", expand=True)
        self.chat_box.tag_config("user", foreground="#6c63ff", font=("Helvetica", 11, "bold"))
        self.chat_box.tag_config("assistant", foreground="#2ecc71", font=("Helvetica", 11))

        input_frame = tk.Frame(self.root, bg="#0f0f1a", padx=20, pady=8)
        input_frame.pack(fill="x")
        self.text_input = tk.Entry(input_frame, font=("Helvetica", 12), bg="#1a1a2e", fg="white", insertbackground="white", relief="flat", bd=8)
        self.text_input.pack(side="left", fill="x", expand=True, ipady=6)
        self.text_input.bind("<Return>", self.send_text)
        tk.Button(input_frame, text="Send", font=("Helvetica", 11, "bold"), bg="#6c63ff", fg="white", relief="flat", padx=12, cursor="hand2", command=self.send_text).pack(side="left", padx=(8, 0))

        self.mic_btn = tk.Button(self.root, text="Click to Speak", font=("Helvetica", 14, "bold"), bg="#6c63ff", fg="white", relief="flat", padx=20, pady=14, cursor="hand2", command=self.toggle_listen)
        self.mic_btn.pack(pady=12)

        quick_frame = tk.Frame(self.root, bg="#0f0f1a", padx=20)
        quick_frame.pack(fill="x", pady=(0, 12))
        tk.Label(quick_frame, text="Quick Commands:", font=("Helvetica", 9), bg="#0f0f1a", fg="#555").pack(anchor="w")
        btn_row = tk.Frame(quick_frame, bg="#0f0f1a")
        btn_row.pack(fill="x")
        for label, cmd in [("Time", "time"), ("Date", "date"), ("Joke", "joke"), ("Help", "help")]:
            tk.Button(btn_row, text=label, font=("Helvetica", 9), bg="#2a2a3e", fg="white", relief="flat", padx=10, pady=5, cursor="hand2", command=lambda c=cmd: self.run_command(c)).pack(side="left", padx=3)

    def greet(self):
        greeting = process_command("hello")
        self.display_message("Assistant", greeting, "assistant")
        threading.Thread(target=speak, args=(greeting,), daemon=True).start()

    def toggle_listen(self):
        if not self.is_listening:
            threading.Thread(target=self.listen_and_respond, daemon=True).start()

    def listen_and_respond(self):
        self.is_listening = True
        self.update_status("Listening...", "#e74c3c")
        self.mic_btn.config(text="Listening...", bg="#e74c3c")
        command = listen()
        self.update_status("Processing...", "#f39c12")
        self.mic_btn.config(text="Processing...", bg="#f39c12")
        if command not in ("timeout", "unknown", "error"):
            self.display_message("You", command, "user")
        response = process_command(command)
        self.display_message("Assistant", response, "assistant")
        threading.Thread(target=speak, args=(response,), daemon=True).start()
        self.is_listening = False
        self.update_status("Ready", "#2ecc71")
        self.mic_btn.config(text="Click to Speak", bg="#6c63ff")
        if any(word in command for word in ["bye", "goodbye", "exit"]):
            self.root.aft5er(2000, self.root.destroy)

    def send_text(self, event=None):
        command = self.text_input.get().strip().lower()
        if not command:
            return
        self.text_input.delete(0, tk.END)
        self.display_message("You", command, "user")
        response = process_command(command)
        self.display_message("Assistant", response, "assistant")
        threading.Thread(target=speak, args=(response,), daemon=True).start()

    def run_command(self, command):
        self.display_message("You", command, "user")
        response = process_command(command)
        self.display_message("Assistant", response, "assistant")
        threading.Thread(target=speak, args=(response,), daemon=True).start()

    def display_message(self, sender, message, tag):
        self.chat_box.config(state="normal")
        self.chat_box.insert(tk.END, f"{sender}: ", tag)
        self.chat_box.insert(tk.END, f"{message}\n\n")
        self.chat_box.config(state="disabled")
        self.chat_box.see(tk.END)

    def update_status(self, text, color):
        self.status_label.config(text=text, fg=color)
        self.status_dot.config(fg=color)


if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceAssistantApp(root)
    root.mainloop()
