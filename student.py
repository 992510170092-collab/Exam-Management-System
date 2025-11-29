import tkinter as tk
from tkinter import messagebox
import pymysql
import sys
import subprocess
import os

# --- Database Connection ---
def connect_db():
    return pymysql.connect(
        host="localhost",
        user="root",                       # your MySQL username
        password="nikki@13#18@#",          # your MySQL password
        database="DBMS"                    # your database name
    )

# --- View Results ---
def view_results(username):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username=%s", (username,))
        user_id = cursor.fetchone()[0]

        cursor.execute("SELECT score FROM quiz_results WHERE user_id=%s", (user_id,))
        results = cursor.fetchall()
        conn.close()

        if results:
            result_win = tk.Toplevel(root)
            result_win.title("Your Quiz Results")
            result_win.geometry("300x250")

            tk.Label(result_win, text=f"Results for {username}", font=("Helvetica", 14, "bold")).pack(pady=10)

            frame = tk.Frame(result_win)
            frame.pack(pady=10)
            tk.Label(frame, text="Score", width=10, borderwidth=1, relief="solid").grid(row=0, column=0)

            for i, (score,) in enumerate(results, start=1):
                tk.Label(frame, text=str(score), width=10, borderwidth=1, relief="solid").grid(row=i, column=0)
        else:
            messagebox.showinfo("Your Results", "No quiz results found.")

    except Exception as e:
        messagebox.showerror("Error", f"Could not fetch results: {e}")


# --- Edit Profile ---
def edit_profile(username):
    edit_win = tk.Toplevel(root)
    edit_win.title("Edit Profile")
    edit_win.geometry("300x200")

    tk.Label(edit_win, text="New Password").pack(pady=5)
    entry_pass = tk.Entry(edit_win, show="*")
    entry_pass.pack(pady=5)

    def update_password():
        new_pass = entry_pass.get()
        if not new_pass:
            messagebox.showwarning("Input Error", "Password cannot be empty.")
            return
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET password=%s WHERE username=%s", (new_pass, username))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Password updated successfully!")
            edit_win.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Update failed: {e}")

    tk.Button(edit_win, text="Update", command=update_password).pack(pady=10)

# --- Take Quiz ---
def take_quiz(username):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    subprocess.Popen([sys.executable, os.path.join(base_dir, "quiz.py"), username])

# --- Logout ---
def logout():
    root.destroy()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    subprocess.Popen([sys.executable, os.path.join(base_dir, "login.py")])

# --- GUI Setup ---
username = sys.argv[1] if len(sys.argv) > 1 else "Student"

root = tk.Tk()
root.title("Student Dashboard")
root.geometry("400x300")
root.configure(bg="#1e1e1e")

tk.Label(root, text=f"Welcome, {username}", font=("Helvetica", 14, "bold"), fg="white", bg="#1e1e1e").pack(pady=20)

tk.Button(root, text="Take Quiz", command=lambda: take_quiz(username), width=20, bg="#6a0dad", fg="white").pack(pady=10)
tk.Button(root, text="View Results", command=lambda: view_results(username), width=20, bg="#1976d2", fg="white").pack(pady=10)
tk.Button(root, text="Edit Profile", command=lambda: edit_profile(username), width=20, bg="#388e3c", fg="white").pack(pady=10)
tk.Button(root, text="Logout", command=logout, width=20, bg="#d32f2f", fg="white").pack(pady=10)

root.mainloop()
