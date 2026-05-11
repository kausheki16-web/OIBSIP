import tkinter as tk
from tkinter import messagebox
import random
import string
import pyperclip
from datetime import datetime

# ---------------- PASSWORD GENERATOR ---------------- #

def generate_password():

    try:
        length = int(length_entry.get())

        if length < 4:
            messagebox.showerror("Error", "Password length must be at least 4.")
            return

        characters = ""

        if uppercase_var.get():
            characters += string.ascii_uppercase

        if lowercase_var.get():
            characters += string.ascii_lowercase

        if numbers_var.get():
            characters += string.digits

        if symbols_var.get():
            characters += string.punctuation

        if exclude_var.get():
            confusing = "0O1lI"
            characters = ''.join(c for c in characters if c not in confusing)

        if not characters:
            messagebox.showerror("Error", "Select at least one character type.")
            return

        password = ''.join(random.choice(characters) for _ in range(length))

        password_entry.delete(0, tk.END)
        password_entry.insert(0, password)

        strength = check_strength(password)

        strength_label.config(
            text=f"Strength: {strength}",
            fg=get_strength_color(strength)
        )

        save_history(password, strength)

    except ValueError:
        messagebox.showerror("Error", "Enter a valid number.")

# ---------------- PASSWORD STRENGTH ---------------- #

def check_strength(password):

    score = 0

    if any(c.islower() for c in password):
        score += 1

    if any(c.isupper() for c in password):
        score += 1

    if any(c.isdigit() for c in password):
        score += 1

    if any(c in string.punctuation for c in password):
        score += 1

    if len(password) >= 12:
        score += 1

    if score <= 2:
        return "Weak"
    elif score <= 4:
        return "Medium"
    else:
        return "Strong"

# ---------------- STRENGTH COLOR ---------------- #

def get_strength_color(strength):

    if strength == "Weak":
        return "red"

    elif strength == "Medium":
        return "orange"

    else:
        return "green"

# ---------------- COPY PASSWORD ---------------- #

def copy_password():

    password = password_entry.get()

    if password:
        pyperclip.copy(password)
        messagebox.showinfo("Copied", "Password copied to clipboard.")
    else:
        messagebox.showwarning("Warning", "No password to copy.")

# ---------------- SAVE HISTORY ---------------- #

def save_history(password, strength):

    with open("password_history.txt", "a") as file:
        file.write(
            f"{datetime.now()} | {password} | {strength}\n"
        )

# ---------------- VIEW HISTORY ---------------- #

def view_history():

    try:
        history_window = tk.Toplevel(root)
        history_window.title("Password History")
        history_window.geometry("600x400")

        text_area = tk.Text(history_window)
        text_area.pack(fill=tk.BOTH, expand=True)

        with open("password_history.txt", "r") as file:
            text_area.insert(tk.END, file.read())

    except FileNotFoundError:
        messagebox.showinfo("Info", "No history found.")

# ---------------- GUI ---------------- #

root = tk.Tk()
root.title("Advanced Password Generator")
root.geometry("500x600")
root.config(bg="#f4f4f4")

# Title
title = tk.Label(
    root,
    text="Advanced Password Generator",
    font=("Arial", 20, "bold"),
    bg="#f4f4f4",
    fg="darkblue"
)
title.pack(pady=20)

# Length
tk.Label(
    root,
    text="Password Length",
    font=("Arial", 12),
    bg="#f4f4f4"
).pack()

length_entry = tk.Entry(root, font=("Arial", 12), width=10)
length_entry.pack(pady=5)
length_entry.insert(0, "12")

# Checkboxes
uppercase_var = tk.BooleanVar(value=True)
lowercase_var = tk.BooleanVar(value=True)
numbers_var = tk.BooleanVar(value=True)
symbols_var = tk.BooleanVar(value=True)
exclude_var = tk.BooleanVar()

tk.Checkbutton(
    root,
    text="Include Uppercase Letters",
    variable=uppercase_var,
    bg="#f4f4f4"
).pack(anchor='w', padx=100)

tk.Checkbutton(
    root,
    text="Include Lowercase Letters",
    variable=lowercase_var,
    bg="#f4f4f4"
).pack(anchor='w', padx=100)

tk.Checkbutton(
    root,
    text="Include Numbers",
    variable=numbers_var,
    bg="#f4f4f4"
).pack(anchor='w', padx=100)

tk.Checkbutton(
    root,
    text="Include Symbols",
    variable=symbols_var,
    bg="#f4f4f4"
).pack(anchor='w', padx=100)

tk.Checkbutton(
    root,
    text="Exclude Confusing Characters (0,O,1,l,I)",
    variable=exclude_var,
    bg="#f4f4f4"
).pack(anchor='w', padx=100)

# Generate Button
generate_btn = tk.Button(
    root,
    text="Generate Password",
    font=("Arial", 12, "bold"),
    bg="green",
    fg="white",
    command=generate_password
)
generate_btn.pack(pady=20)

# Password Output
password_entry = tk.Entry(
    root,
    font=("Arial", 14),
    width=30,
    justify="center"
)
password_entry.pack(pady=10)

# Strength Label
strength_label = tk.Label(
    root,
    text="Strength: ",
    font=("Arial", 12, "bold"),
    bg="#f4f4f4"
)
strength_label.pack(pady=5)

# Copy Button
copy_btn = tk.Button(
    root,
    text="Copy Password",
    font=("Arial", 11),
    bg="blue",
    fg="white",
    command=copy_password
)
copy_btn.pack(pady=10)

# History Button
history_btn = tk.Button(
    root,
    text="View Password History",
    font=("Arial", 11),
    bg="purple",
    fg="white",
    command=view_history
)
history_btn.pack(pady=10)

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