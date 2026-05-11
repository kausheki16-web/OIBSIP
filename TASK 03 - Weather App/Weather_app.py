import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
from io import BytesIO

# ---------------- API KEY ---------------- #

API_KEY = "edb99034c09c7374c0832b76e71ba048"

# ---------------- FETCH WEATHER ---------------- #

def get_weather():

    city = city_entry.get()

    if city == "":
        messagebox.showerror("Error", "Please enter a city name.")
        return

    unit = unit_var.get()

    if unit == "Celsius":
        units = "metric"
        temp_symbol = "°C"
    else:
        units = "imperial"
        temp_symbol = "°F"

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units={units}"

    try:
        response = requests.get(url)
        data = response.json()

        if data["cod"] != 200:
            messagebox.showerror("Error", "City not found.")
            return

        # Weather Data
        city_name = data["name"]
        country = data["sys"]["country"]

        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]

        weather = data["weather"][0]["description"].title()
        wind_speed = data["wind"]["speed"]

        icon_code = data["weather"][0]["icon"]

        # Update Labels
        location_label.config(
            text=f"{city_name}, {country}"
        )

        temp_label.config(
            text=f"{temperature}{temp_symbol}"
        )

        weather_label.config(
            text=weather
        )

        details_label.config(
            text=f"Humidity: {humidity}%\n"
                 f"Pressure: {pressure} hPa\n"
                 f"Wind Speed: {wind_speed}"
        )

        # Weather Icon
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"

        icon_response = requests.get(icon_url)

        img_data = icon_response.content

        image = Image.open(BytesIO(img_data))
        photo = ImageTk.PhotoImage(image)

        icon_label.config(image=photo)
        icon_label.image = photo

    except Exception as e:
        messagebox.showerror("Error", str(e))

# ---------------- GUI ---------------- #

root = tk.Tk()
root.title("Advanced Weather App")
root.geometry("500x650")
root.config(bg="#87CEEB")

# Title
title = tk.Label(
    root,
    text="Weather App",
    font=("Arial", 24, "bold"),
    bg="#87CEEB",
    fg="white"
)
title.pack(pady=20)

# City Entry
city_entry = tk.Entry(
    root,
    font=("Arial", 14),
    width=25,
    justify="center"
)
city_entry.pack(pady=10)

# Unit Selection
unit_var = tk.StringVar(value="Celsius")

unit_frame = tk.Frame(root, bg="#87CEEB")
unit_frame.pack()

tk.Radiobutton(
    unit_frame,
    text="Celsius",
    variable=unit_var,
    value="Celsius",
    bg="#87CEEB",
    font=("Arial", 11)
).pack(side=tk.LEFT, padx=10)

tk.Radiobutton(
    unit_frame,
    text="Fahrenheit",
    variable=unit_var,
    value="Fahrenheit",
    bg="#87CEEB",
    font=("Arial", 11)
).pack(side=tk.LEFT, padx=10)

# Search Button
search_btn = tk.Button(
    root,
    text="Get Weather",
    font=("Arial", 12, "bold"),
    bg="blue",
    fg="white",
    command=get_weather
)
search_btn.pack(pady=20)

# Weather Icon
icon_label = tk.Label(root, bg="#87CEEB")
icon_label.pack()

# Location
location_label = tk.Label(
    root,
    text="",
    font=("Arial", 20, "bold"),
    bg="#87CEEB",
    fg="white"
)
location_label.pack(pady=10)

# Temperature
temp_label = tk.Label(
    root,
    text="",
    font=("Arial", 40, "bold"),
    bg="#87CEEB",
    fg="white"
)
temp_label.pack()

# Weather Description
weather_label = tk.Label(
    root,
    text="",
    font=("Arial", 18),
    bg="#87CEEB",
    fg="white"
)
weather_label.pack(pady=10)

# Weather Details
details_label = tk.Label(
    root,
    text="",
    font=("Arial", 14),
    bg="#87CEEB",
    fg="white",
    justify="left"
)
details_label.pack(pady=20)

# Exit Button
exit_btn = tk.Button(
    root,
    text="Exit",
    font=("Arial", 11),
    bg="red",
    fg="white",
    command=root.quit
)
exit_btn.pack(pady=20)

root.mainloop()