# Auto-install required packages
import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Try importing and install if not present
try:
    import customtkinter as ctk
except ImportError:
    install("customtkinter")
    import customtkinter as ctk

try:
    import requests
except ImportError:
    install("requests")
    import requests

import tkinter.messagebox as messagebox

# ---- Main Application ----
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("400x430")
app.title("Login Generator")

# Global variable to store credentials
generated_credentials = ""

def generate_login():
    global generated_credentials

    email = email_entry.get()
    name = name_entry.get()
    username = username_entry.get()

    if not email or not name or not username:
        result_label.configure(text="All fields are required.", text_color="red")
        return

    url = f"http://141.147.118.157:5678/webhook/03d776ed-329e-495a-b5bc-792c8c606c6f45?username={username}&email={email}&name={name}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            generated_credentials = f"Username: {data['username']}\nPassword: {data['password']}"
            result_label.configure(text=generated_credentials, text_color="green")
        else:
            result_label.configure(
                text=f"Error: {response.status_code} - {response.text}",
                text_color="red"
            )
    except Exception as e:
        result_label.configure(text=f"Exception: {str(e)}", text_color="red")

def copy_to_clipboard():
    if generated_credentials:
        app.clipboard_clear()
        app.clipboard_append(generated_credentials)
        messagebox.showinfo("Copied", "Username and password copied to clipboard.")
    else:
        messagebox.showwarning("Nothing to Copy", "Generate login first.")

# UI Elements
ctk.CTkLabel(app, text="Email:").pack(pady=5)
email_entry = ctk.CTkEntry(app, width=300)
email_entry.pack(pady=5)

ctk.CTkLabel(app, text="Name:").pack(pady=5)
name_entry = ctk.CTkEntry(app, width=300)
name_entry.pack(pady=5)

ctk.CTkLabel(app, text="Username:").pack(pady=5)
username_entry = ctk.CTkEntry(app, width=300)
username_entry.pack(pady=5)

ctk.CTkButton(app, text="Generate Login", command=generate_login).pack(pady=10)
ctk.CTkButton(app, text="Copy to Clipboard", command=copy_to_clipboard).pack(pady=5)

result_label = ctk.CTkLabel(app, text="", font=ctk.CTkFont(size=14), wraplength=350)
result_label.pack(pady=10)

app.mainloop()
