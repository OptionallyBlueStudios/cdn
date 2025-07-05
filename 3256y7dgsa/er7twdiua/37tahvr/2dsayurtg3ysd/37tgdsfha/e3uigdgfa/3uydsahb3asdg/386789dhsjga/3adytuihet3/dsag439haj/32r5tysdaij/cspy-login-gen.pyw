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

# ---- Main Application ----
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("400x400")
app.title("Login Generator")

def generate_login():
    email = email_entry.get()
    name = name_entry.get()
    username = username_entry.get()

    if not email or not name or not username:
        result_label.configure(text="All fields are required.", text_color="red")
        return

    url = f"http://141.147.118.157:5678/webhook/03d776ed-329e-495a-b5bc-792c8c606c6f?username={username}&email={email}&name={name}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            result_label.configure(
                text=f"Username: {data['username']}\nPassword: {data['password']}",
                text_color="green"
            )
        else:
            result_label.configure(
                text=f"Error: {response.status_code} - {response.text}",
                text_color="red"
            )
    except Exception as e:
        result_label.configure(text=f"Exception: {str(e)}", text_color="red")

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

ctk.CTkButton(app, text="Generate Login", command=generate_login).pack(pady=20)

result_label = ctk.CTkLabel(app, text="", font=ctk.CTkFont(size=14))
result_label.pack(pady=10)

app.mainloop()
