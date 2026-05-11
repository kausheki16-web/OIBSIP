import tkinter as tk
from tkinter import messagebox
import csv
import os
from datetime import datetime
import matplotlib.pyplot as plt

FILE_NAME = "bmi_data.csv"

# ---------------- BMI CALCULATION ---------------- #

def calculate_bmi():
    try:
        name = name_entry.get()

        weight = float(weight_entry.get())
        height = float(height_entry.get())

        if weight <= 0 or height <= 0:
            messagebox.showerror("Invalid Input", "Weight and Height must be positive.")
            return

        bmi = weight / (height ** 2)
        bmi = round(bmi, 2)

        category = get_category(bmi)

        result_label.config(
            text=f"BMI: {bmi}\nCategory: {category}",
            fg="blue"
        )

        save_data(name, weight, height, bmi, category)

    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers.")

# ---------------- BMI CATEGORY ---------------- #

def get_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 24.9:
        return "Normal Weight"
    elif bmi < 29.9:
        return "Overweight"
    else:
        return "Obese"

# ---------------- SAVE DATA ---------------- #

def save_data(name, weight, height, bmi, category):

    file_exists = os.path.isfile(FILE_NAME)

    with open(FILE_NAME, mode='a', newline='') as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["Date", "Name", "Weight", "Height", "BMI", "Category"])

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            name,
            weight,
            height,
            bmi,
            category
        ])

# ---------------- VIEW HISTORY ---------------- #

def view_history():

    if not os.path.exists(FILE_NAME):
        messagebox.showinfo("No Data", "No BMI history found.")
        return

    history_window = tk.Toplevel(root)
    history_window.title("BMI History")
    history_window.geometry("700x400")

    text_area = tk.Text(history_window)
    text_area.pack(fill=tk.BOTH, expand=True)

    with open(FILE_NAME, 'r') as file:
        data = file.read()
        text_area.insert(tk.END, data)

# ---------------- SHOW GRAPH ---------------- #

def show_graph():

    if not os.path.exists(FILE_NAME):
        messagebox.showinfo("No Data", "No data available for graph.")
        return

    dates = []
    bmi_values = []

    with open(FILE_NAME, 'r') as file:
        reader = csv.DictReader(file)

        for row in reader:
            dates.append(row['Date'])
            bmi_values.append(float(row['BMI']))

    plt.figure(figsize=(10, 5))
    plt.plot(dates, bmi_values, marker='o')

    plt.title("BMI Trend Analysis")
    plt.xlabel("Date")
    plt.ylabel("BMI")

    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.show()

# ---------------- GUI ---------------- #

root = tk.Tk()
root.title("Advanced BMI Calculator")
root.geometry("450x500")
root.config(bg="#f0f0f0")

title = tk.Label(
    root,
    text="Advanced BMI Calculator",
    font=("Arial", 20, "bold"),
    bg="#f0f0f0",
    fg="darkgreen"
)
title.pack(pady=20)

# Name
tk.Label(root, text="Name", bg="#f0f0f0", font=("Arial", 12)).pack()
name_entry = tk.Entry(root, width=30, font=("Arial", 12))
name_entry.pack(pady=5)

# Weight
tk.Label(root, text="Weight (kg)", bg="#f0f0f0", font=("Arial", 12)).pack()
weight_entry = tk.Entry(root, width=30, font=("Arial", 12))
weight_entry.pack(pady=5)

# Height
tk.Label(root, text="Height (m)", bg="#f0f0f0", font=("Arial", 12)).pack()
height_entry = tk.Entry(root, width=30, font=("Arial", 12))
height_entry.pack(pady=5)

# Calculate Button
calc_btn = tk.Button(
    root,
    text="Calculate BMI",
    font=("Arial", 12, "bold"),
    bg="green",
    fg="white",
    command=calculate_bmi
)
calc_btn.pack(pady=15)

# Result
result_label = tk.Label(
    root,
    text="",
    font=("Arial", 14, "bold"),
    bg="#f0f0f0"
)
result_label.pack(pady=10)

# History Button
history_btn = tk.Button(
    root,
    text="View History",
    font=("Arial", 11),
    bg="blue",
    fg="white",
    command=view_history
)
history_btn.pack(pady=10)

# Graph Button
graph_btn = tk.Button(
    root,
    text="Show BMI Graph",
    font=("Arial", 11),
    bg="purple",
    fg="white",
    command=show_graph
)
graph_btn.pack(pady=10)

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