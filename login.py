import tkinter as tk
from tkinter import messagebox, ttk
import pymysql
import subprocess
import sys
import os

# --- Verify Login ---
def verify_login(username, password, role):
    try:
        conn = pymysql.connect(
            host="localhost",
            user="root",                       # your MySQL username
            password="nikki@13#18@#",          # your MySQL password
            database="DBMS"                    # your database name
        )
        cursor = conn.cursor()

        query = "SELECT * FROM users WHERE username=%s AND password=%s AND user_type=%s"
        cursor.execute(query, (username, password, role))
        result = cursor.fetchone()

        if result:
            messagebox.showinfo("Login", f"Welcome {role.capitalize()} {username}!")
            root.destroy()  # Close login window

            # Launch appropriate dashboard
            base_dir = os.path.dirname(os.path.abspath(__file__))
            if role == "student":
                subprocess.Popen([sys.executable, os.path.join(base_dir, "student.py"), username])
            elif role == "teacher":
                subprocess.Popen([sys.executable, os.path.join(base_dir, "teacher.py"), username])
        else:
            messagebox.showerror("Login", "Invalid credentials or role mismatch.")

    except Exception as err:
        messagebox.showerror("Error", f"Database error: {err}")
    finally:
        if conn and conn.open:
            conn.close()

# --- Login Button Action ---
def login():
    user = entry_user.get()
    pwd = entry_pass.get()
    role = role_var.get()
    if not user or not pwd:
        messagebox.showwarning("Input Error", "Please enter both username and password.")
        return
    verify_login(user, pwd, role)

# --- Quit Button Action ---
def quit_app():
    root.destroy()

# --- GUI Setup ---
root = tk.Tk()
root.title("LOGIN")
root.geometry("400x300")
root.configure(bg="#1e1e1e")  # Dark background

# --- Styling ---
label_font = ("Helvetica", 12, "bold")
entry_font = ("Helvetica", 11)
button_font = ("Helvetica", 12, "bold")

# --- Username ---
tk.Label(root, text="User Name", font=label_font, fg="white", bg="#1e1e1e").pack(pady=(20, 5))
entry_user = tk.Entry(root, font=entry_font, width=30, bg="#2e2e2e", fg="white", insertbackground="white")
entry_user.pack()

# --- Password ---
tk.Label(root, text="Password", font=label_font, fg="white", bg="#1e1e1e").pack(pady=(10, 5))
entry_pass = tk.Entry(root, show="*", font=entry_font, width=30, bg="#2e2e2e", fg="white", insertbackground="white")
entry_pass.pack()

# --- Role Dropdown ---
tk.Label(root, text="Type", font=label_font, fg="white", bg="#1e1e1e").pack(pady=(10, 5))
role_var = tk.StringVar(value="student")
role_dropdown = ttk.Combobox(root, textvariable=role_var, values=["student", "teacher"], state="readonly", font=entry_font, width=28)
role_dropdown.pack()

# --- Buttons ---
frame_buttons = tk.Frame(root, bg="#1e1e1e")
frame_buttons.pack(pady=20)

tk.Button(frame_buttons, text="Login", command=login, font=button_font, bg="#6a0dad", fg="white", width=12).grid(row=0, column=0, padx=10)
tk.Button(frame_buttons, text="Quit", command=quit_app, font=button_font, bg="#d32f2f", fg="white", width=12).grid(row=0, column=1, padx=10)

root.mainloop()
