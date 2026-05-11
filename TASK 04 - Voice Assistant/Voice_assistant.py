import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import pywhatkit
import pyjokes
import webbrowser
import requests
import tkinter as tk
from tkinter import scrolledtext
import threading

# New Libraries
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np

# ---------------- TEXT TO SPEECH ---------------- #

engine = pyttsx3.init()

voices = engine.getProperty('voices')

engine.setProperty('voice', voices[1].id)

engine.setProperty('rate', 170)

# ---------------- GUI OUTPUT FUNCTION ---------------- #

def update_output(text):

    output_area.insert(
        tk.END,
        text + "\n"
    )

    output_area.see(tk.END)

# ---------------- SPEAK FUNCTION ---------------- #

def speak(text):

    update_output("Assistant: " + text)

    engine.say(text)

    engine.runAndWait()

# ---------------- SPEECH RECOGNITION ---------------- #

listener = sr.Recognizer()

# Record Audio Without PyAudio
def record_audio():

    fs = 44100
    seconds = 5

    update_output("Listening...")

    recording = sd.rec(
        int(seconds * fs),
        samplerate=fs,
        channels=1,
        dtype='int16'
    )

    sd.wait()

    write("voice.wav", fs, recording)

# Convert Speech To Text
def listen():

    try:

        record_audio()

        with sr.AudioFile("voice.wav") as source:

            audio = listener.record(source)

            command = listener.recognize_google(audio)

            command = command.lower()

            update_output("You: " + command)

            return command

    except Exception as e:

        update_output(f"Error: {e}")

        return ""

# ---------------- WEATHER FUNCTION ---------------- #

def get_weather(city):

    api_key = "edb99034c09c7374c0832b76e71ba048"

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    response = requests.get(url)

    data = response.json()

    if data["cod"] != 200:

        speak("City not found")

        return

    temp = data["main"]["temp"]

    weather = data["weather"][0]["description"]

    speak(
        f"The temperature is {temp} degree Celsius with {weather}"
    )

# ---------------- MAIN ASSISTANT FUNCTION ---------------- #

def run_assistant():

    command = listen()

    if command == "":
        speak("I could not hear properly.")
        return

    if "hello" in command:

        speak("Hello, how can I help you?")

    elif "time" in command:

        current_time = datetime.datetime.now().strftime('%I:%M %p')

        speak("Current time is " + current_time)

    elif "date" in command:

        current_date = datetime.datetime.now().strftime('%d %B %Y')

        speak("Today's date is " + current_date)

    elif "wikipedia" in command:

        try:

            topic = command.replace("wikipedia", "")

            info = wikipedia.summary(topic, sentences=2)

            speak(info)

        except:

            speak("Could not find information.")

    elif "play" in command:

        song = command.replace("play", "")

        speak("Playing " + song)

        pywhatkit.playonyt(song)

    elif "open youtube" in command:

        webbrowser.open("https://www.youtube.com")

        speak("Opening YouTube")

    elif "open google" in command:

        webbrowser.open("https://www.google.com")

        speak("Opening Google")

    elif "joke" in command:

        joke = pyjokes.get_joke()

        speak(joke)

    elif "weather" in command:

        speak("Tell me city name")

        city = listen()

        if city != "":
            get_weather(city)

    elif "exit" in command:

        speak("Goodbye")

        root.destroy()

    else:

        speak("Sorry, I did not understand.")

# ---------------- THREADING ---------------- #

def start_assistant():

    thread = threading.Thread(
        target=run_assistant
    )

    thread.start()

# ---------------- GUI ---------------- #

root = tk.Tk()

root.title("Advanced Voice Assistant")

root.geometry("700x600")

root.config(bg="#1E1E1E")

# Title
title = tk.Label(
    root,
    text="AI Voice Assistant",
    font=("Arial", 24, "bold"),
    bg="#1E1E1E",
    fg="white"
)

title.pack(pady=20)

# Output Area
output_area = scrolledtext.ScrolledText(
    root,
    font=("Arial", 12),
    bg="#2D2D2D",
    fg="white"
)

output_area.pack(
    padx=20,
    pady=20,
    fill=tk.BOTH,
    expand=True
)

# Start Button
listen_button = tk.Button(
    root,
    text="Start Listening",
    font=("Arial", 14, "bold"),
    bg="green",
    fg="white",
    command=start_assistant
)

listen_button.pack(pady=20)

# Exit Button
exit_button = tk.Button(
    root,
    text="Exit",
    font=("Arial", 12, "bold"),
    bg="red",
    fg="white",
    command=root.destroy
)

exit_button.pack(pady=10)

# ---------------- MAIN LOOP ---------------- #

root.mainloop()