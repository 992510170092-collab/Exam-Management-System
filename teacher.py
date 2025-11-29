import tkinter as tk
from tkinter import messagebox, ttk
import pymysql
import sys
import subprocess
import os

# --- Database Connection ---
def connect_db():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="nikki@13#18@#",
        database="DBMS"
    )

# --- Combined Question Management ---
def manage_questions(root):
    mgmt_win = tk.Toplevel(root)
    mgmt_win.title("Question Management")
    mgmt_win.geometry("600x600")
    
    # Tab control
    tab_control = ttk.Notebook(mgmt_win)
    
    # Add Question Tab
    add_tab = ttk.Frame(tab_control)
    tab_control.add(add_tab, text="Add Question")
    
    # View/Edit/Delete Tab
    manage_tab = ttk.Frame(tab_control)
    tab_control.add(manage_tab, text="Manage Questions")
    
    tab_control.pack(expand=1, fill="both")
    
    # === ADD QUESTION TAB ===
    tk.Label(add_tab, text="Question Text:").pack(pady=5)
    entry_q = tk.Text(add_tab, height=3, width=60)
    entry_q.pack(pady=5)
    
    options = []
    for i in range(4):
        tk.Label(add_tab, text=f"Option {i+1}:").pack(pady=2)
        e = tk.Entry(add_tab, width=60)
        e.pack(pady=2)
        options.append(e)
    
    tk.Label(add_tab, text="Correct Option (1-4):").pack(pady=5)
    entry_correct = tk.Entry(add_tab, width=5)
    entry_correct.pack(pady=5)
    
    def save_question():
        q = entry_q.get("1.0", tk.END).strip()
        opt = [o.get().strip() for o in options]
        correct = entry_correct.get().strip()
        
        if not q or not all(opt) or not correct.isdigit() or not (1 <= int(correct) <= 4):
            messagebox.showwarning("Input Error", "Please fill all fields correctly.\nCorrect option must be 1-4.")
            return
        
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("""INSERT INTO questions 
                (question_text, option1, option2, option3, option4, correct_option) 
                VALUES (%s,%s,%s,%s,%s,%s)""", 
                (q, opt[0], opt[1], opt[2], opt[3], int(correct)))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Question added successfully!")
            # Clear fields
            entry_q.delete("1.0", tk.END)
            for o in options:
                o.delete(0, tk.END)
            entry_correct.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"Could not add question: {e}")
    
    tk.Button(add_tab, text="Save Question", command=save_question, bg="#388e3c", fg="white").pack(pady=20)
    
    # === MANAGE QUESTIONS TAB ===
    def load_questions_table():
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT id, question_text, option1, option2, option3, option4, correct_option FROM questions ORDER BY id")
            questions = cursor.fetchall()
            conn.close()
            
            # Clear table
            for row in questions_tree.get_children():
                questions_tree.delete(row)
                
            # Add questions to table
            for q in questions:
                questions_tree.insert("", "end", values=q)
                
        except Exception as e:
            messagebox.showerror("Error", f"Could not load questions: {e}")
    
    # Questions table
    table_frame = tk.Frame(manage_tab)
    table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Create treeview for questions
    columns = ("ID", "Question", "Option1", "Option2", "Option3", "Option4", "Correct")
    questions_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)
    
    # Define headings
    questions_tree.heading("ID", text="ID")
    questions_tree.heading("Question", text="Question")
    questions_tree.heading("Option1", text="Option 1")
    questions_tree.heading("Option2", text="Option 2")
    questions_tree.heading("Option3", text="Option 3")
    questions_tree.heading("Option4", text="Option 4")
    questions_tree.heading("Correct", text="Correct")
    
    # Set column widths
    questions_tree.column("ID", width=50)
    questions_tree.column("Question", width=200)
    questions_tree.column("Option1", width=100)
    questions_tree.column("Option2", width=100)
    questions_tree.column("Option3", width=100)
    questions_tree.column("Option4", width=100)
    questions_tree.column("Correct", width=60)
    
    # Scrollbar for table
    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=questions_tree.yview)
    questions_tree.configure(yscrollcommand=scrollbar.set)
    
    questions_tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Action buttons
    btn_frame = tk.Frame(manage_tab)
    btn_frame.pack(fill=tk.X, padx=10, pady=10)
    
    def delete_selected():
        selection = questions_tree.selection()
        if not selection:
            messagebox.showwarning("Selection Error", "Please select a question to delete.")
            return
        
        item = questions_tree.item(selection[0])
        qid = item['values'][0]
        
        if messagebox.askyesno("Confirm Delete", f"Delete question ID {qid}?"):
            try:
                conn = connect_db()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM questions WHERE id=%s", (qid,))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", f"Question ID {qid} deleted.")
                load_questions_table()
            except Exception as e:
                messagebox.showerror("Error", f"Could not delete question: {e}")
    
    def update_selected():
        selection = questions_tree.selection()
        if not selection:
            messagebox.showwarning("Selection Error", "Please select a question to update.")
            return
        
        item = questions_tree.item(selection[0])
        values = item['values']
        open_update_window(values)
    
    def open_update_window(question_data):
        update_win = tk.Toplevel(mgmt_win)
        update_win.title("Update Question")
        update_win.geometry("500x400")
        
        tk.Label(update_win, text=f"Updating Question ID: {question_data[0]}", font=("Helvetica", 12, "bold")).pack(pady=10)
        
        tk.Label(update_win, text="Question Text:").pack(pady=5)
        entry_q = tk.Text(update_win, height=3, width=50)
        entry_q.pack(pady=5)
        entry_q.insert("1.0", question_data[1])
        
        options = []
        for i in range(4):
            tk.Label(update_win, text=f"Option {i+1}:").pack(pady=2)
            e = tk.Entry(update_win, width=50)
            e.pack(pady=2)
            e.insert(0, question_data[i+2])
            options.append(e)
        
        tk.Label(update_win, text="Correct Option (1-4):").pack(pady=5)
        entry_correct = tk.Entry(update_win, width=5)
        entry_correct.pack(pady=5)
        entry_correct.insert(0, str(question_data[6]))
        
        def save_update():
            q = entry_q.get("1.0", tk.END).strip()
            opt = [o.get().strip() for o in options]
            correct = entry_correct.get().strip()
            
            if not q or not all(opt) or not correct.isdigit() or not (1 <= int(correct) <= 4):
                messagebox.showwarning("Input Error", "Please fill all fields correctly.\nCorrect option must be 1-4.")
                return
            
            try:
                conn = connect_db()
                cursor = conn.cursor()
                cursor.execute("""UPDATE questions 
                                SET question_text=%s, option1=%s, option2=%s, option3=%s, option4=%s, correct_option=%s 
                                WHERE id=%s""",
                            (q, opt[0], opt[1], opt[2], opt[3], int(correct), question_data[0]))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", f"Question ID {question_data[0]} updated successfully!")
                update_win.destroy()
                load_questions_table()
            except Exception as e:
                messagebox.showerror("Error", f"Could not update question: {e}")
        
        tk.Button(update_win, text="Update Question", command=save_update, bg="#ff9800", fg="white").pack(pady=20)
    
    tk.Button(btn_frame, text="View Details", command=lambda: view_selected_details(), bg="#1976d2", fg="white").pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Update Selected", command=update_selected, bg="#ff9800", fg="white").pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Delete Selected", command=delete_selected, bg="#d32f2f", fg="white").pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Refresh List", command=load_questions_table, bg="#6a0dad", fg="white").pack(side=tk.RIGHT, padx=5)
    
    def view_selected_details():
        selection = questions_tree.selection()
        if not selection:
            messagebox.showwarning("Selection Error", "Please select a question to view.")
            return
        
        item = questions_tree.item(selection[0])
        values = item['values']
        
        details_win = tk.Toplevel(mgmt_win)
        details_win.title(f"Question Details - ID {values[0]}")
        details_win.geometry("500x400")
        
        # Create detailed view
        details_frame = tk.Frame(details_win)
        details_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        tk.Label(details_frame, text=f"Question ID: {values[0]}", font=("Helvetica", 12, "bold")).pack(anchor="w", pady=5)
        tk.Label(details_frame, text="Question:", font=("Helvetica", 10, "bold")).pack(anchor="w", pady=(10,2))
        tk.Label(details_frame, text=values[1], wraplength=450, justify="left").pack(anchor="w", pady=2)
        
        tk.Label(details_frame, text="Options:", font=("Helvetica", 10, "bold")).pack(anchor="w", pady=(15,5))
        for i in range(4):
            option_text = f"Option {i+1}: {values[i+2]}"
            if i+1 == values[6]:
                option_text += " ✅ (Correct Answer)"
            tk.Label(details_frame, text=option_text, wraplength=450, justify="left").pack(anchor="w", pady=2)
    
    # Load initial questions
    load_questions_table()

# --- Student Management ---
def manage_students(root):
    stu_win = tk.Toplevel(root)
    stu_win.title("Student Management")
    stu_win.geometry("700x500")
    
    # Add Student Section
    add_frame = tk.LabelFrame(stu_win, text="Add New Student", padx=10, pady=10)
    add_frame.pack(fill=tk.X, padx=10, pady=10)
    
    tk.Label(add_frame, text="Full Name:").pack(anchor="w")
    entry_name = tk.Entry(add_frame, width=40)
    entry_name.pack(fill=tk.X, pady=2)
    
    tk.Label(add_frame, text="Username:").pack(anchor="w")
    entry_user = tk.Entry(add_frame, width=40)
    entry_user.pack(fill=tk.X, pady=2)
    
    tk.Label(add_frame, text="Email:").pack(anchor="w")
    entry_email = tk.Entry(add_frame, width=40)
    entry_email.pack(fill=tk.X, pady=2)
    
    tk.Label(add_frame, text="Password:").pack(anchor="w")
    entry_pass = tk.Entry(add_frame, width=40)
    entry_pass.pack(fill=tk.X, pady=2)
    
    def add_student():
        name = entry_name.get().strip()
        user = entry_user.get().strip()
        email = entry_email.get().strip()
        pwd = entry_pass.get().strip()
        
        if not name or not user or not email or not pwd:
            messagebox.showwarning("Input Error", "All fields are required.")
            return
        
        # Basic email validation
        if "@" not in email or "." not in email:
            messagebox.showwarning("Input Error", "Please enter a valid email address.")
            return
        
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (full_name, username, email, password, user_type) VALUES (%s,%s,%s,%s,%s)",
                         (name, user, email, pwd, "student"))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Student added successfully!")
            # Clear fields
            entry_name.delete(0, tk.END)
            entry_user.delete(0, tk.END)
            entry_email.delete(0, tk.END)
            entry_pass.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"Could not add student: {e}")
    
    tk.Button(add_frame, text="Add Student", command=add_student, bg="#388e3c", fg="white").pack(pady=10)
    
    # View Results Section
    results_frame = tk.LabelFrame(stu_win, text="Student Results", padx=10, pady=10)
    results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Create results table
    columns = ("Name", "Username", "Email", "Score")
    results_tree = ttk.Treeview(results_frame, columns=columns, show="headings", height=10)
    
    # Define headings
    results_tree.heading("Name", text="Student Name")
    results_tree.heading("Username", text="Username")
    results_tree.heading("Email", text="Email")
    results_tree.heading("Score", text="Score")
    
    # Set column widths
    results_tree.column("Name", width=150)
    results_tree.column("Username", width=100)
    results_tree.column("Email", width=150)
    results_tree.column("Score", width=80)
    
    # Scrollbar for table
    scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=results_tree.yview)
    results_tree.configure(yscrollcommand=scrollbar.set)
    
    results_tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    def load_results_table():
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("""SELECT u.full_name, u.username, u.email, r.score 
                              FROM quiz_results r 
                              JOIN users u ON r.user_id = u.id 
                              ORDER BY r.score DESC""")
            results = cursor.fetchall()
            conn.close()
            
            # Clear table
            for row in results_tree.get_children():
                results_tree.delete(row)
                
            # Add results to table
            for result in results:
                results_tree.insert("", "end", values=result)
                
        except Exception as e:
            messagebox.showerror("Error", f"Could not fetch results: {e}")
    
    tk.Button(results_frame, text="Refresh Results", command=load_results_table, bg="#1976d2", fg="white").pack(pady=10)
    
    # Load initial results
    load_results_table()

# --- Logout ---
def logout(root):
    root.destroy()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    subprocess.Popen([sys.executable, os.path.join(base_dir, "login.py")])

# --- GUI Setup ---
username = sys.argv[1] if len(sys.argv) > 1 else "Teacher"

root = tk.Tk()
root.title("Teacher Dashboard")
root.geometry("400x400")
root.configure(bg="#1e1e1e")

tk.Label(root, text=f"Welcome, {username}", font=("Helvetica", 14, "bold"), fg="white", bg="#1e1e1e").pack(pady=20)

tk.Button(root, text="Manage Questions", command=lambda: manage_questions(root), 
          width=20, bg="#6a0dad", fg="white", font=("Helvetica", 11)).pack(pady=10)

tk.Button(root, text="Manage Students", command=lambda: manage_students(root), 
          width=20, bg="#388e3c", fg="white", font=("Helvetica", 11)).pack(pady=10)

tk.Button(root, text="Logout", command=lambda: logout(root), 
          width=20, bg="#d32f2f", fg="white", font=("Helvetica", 11)).pack(pady=20)

root.mainloop()