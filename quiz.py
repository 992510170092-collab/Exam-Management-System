import tkinter as tk
from tkinter import messagebox
import pymysql
import sys
import threading
import time
import cv2
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# --- Database Connection ---
def connect_db():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="nikki@13#18@#", 
        database="DBMS"
    )

# --- Fetch Questions ---
def load_questions():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, question_text, option1, option2, option3, option4, correct_option FROM questions")
    questions = cursor.fetchall()
    conn.close()
    return questions

# --- Save Result ---
def save_result(username, score):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username=%s", (username,))
        user_id = cursor.fetchone()[0]

        cursor.execute("SELECT id FROM quiz_results WHERE user_id=%s", (user_id,))
        existing = cursor.fetchone()

        if existing:
            cursor.execute("UPDATE quiz_results SET score=%s WHERE user_id=%s", (score, user_id))
        else:
            cursor.execute("INSERT INTO quiz_results (user_id, score) VALUES (%s, %s)", (user_id, score))

        conn.commit()
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", f"Could not save result: {e}")

# --- Simplified Proctoring System ---
class SimpleProctoring:
    def __init__(self):
        self.strikes = 0
        self.max_strikes = 3
        self.monitoring_active = True
        self.face_not_detected_time = 0
        self.face_detection_threshold = 3  # seconds
        
        # Proctoring data for graph
        self.cheat_probability = 0
        self.cheat_data = [0] * 50  # Last 50 data points for graph
        
        # Camera
        self.cap = None
        self.init_camera()
        
        # Start monitoring
        self.monitor_thread = threading.Thread(target=self.run_proctoring, daemon=True)
        self.monitor_thread.start()

    def init_camera(self):
        """Initialize camera"""
        try:
            self.cap = cv2.VideoCapture(0)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
            # Load face detection classifier
            self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        except Exception as e:
            print(f"Camera error: {e}")

    def run_proctoring(self):
        """Simple face detection proctoring"""
        while self.monitoring_active and self.cap and self.cap.isOpened():
            try:
                success, frame = self.cap.read()
                if not success:
                    continue
                
                # Convert to grayscale for face detection
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
                
                # Simple logic: if no face detected for threshold time, add strike
                if len(faces) == 0:
                    self.face_not_detected_time += 0.5  # Check every 0.5 seconds
                    self.cheat_probability = min(1.0, self.cheat_probability + 0.1)
                    if self.face_not_detected_time >= self.face_detection_threshold:
                        self.strikes += 1
                        self.face_not_detected_time = 0  # Reset counter
                        print(f"Strike added! Total strikes: {self.strikes}")
                else:
                    self.face_not_detected_time = 0  # Reset if face detected
                    self.cheat_probability = max(0.0, self.cheat_probability - 0.05)
                
                # Update graph data
                self.cheat_data.pop(0)
                self.cheat_data.append(self.cheat_probability)
                    
            except Exception as e:
                print(f"Proctoring error: {e}")
            
            time.sleep(0.5)  # Check every 0.5 seconds

    def get_camera_frame(self):
        """Get current camera frame for display"""
        if self.cap and self.cap.isOpened():
            success, frame = self.cap.read()
            if success:
                # Resize for display
                frame = cv2.resize(frame, (300, 200))
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                return frame
        return None

    def stop_monitoring(self):
        """Stop all monitoring"""
        self.monitoring_active = False
        if self.cap:
            self.cap.release()

# --- Quiz Application with Camera & Graph & Timer ---
class QuizApp:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.questions = load_questions()
        self.index = 0
        self.score = 0
        self.selected_option = tk.IntVar()
        self.user_answers = [0] * len(self.questions)
        
        # Timer variables
        self.time_left = 15  # 15 seconds per question
        self.timer_running = False
        self.timer_id = None
        
        # Initialize proctoring
        self.proctor = SimpleProctoring()
        
        self.setup_ui()
        self.monitor_strikes()
        self.update_camera_display()
        self.update_graph()
        self.display_question()

    def setup_ui(self):
        self.root.title("Proctored Quiz - AI Monitoring Active")
        self.root.geometry("1000x600")
        self.root.configure(bg="#1e1e1e")
        
        # Main container
        main_frame = tk.Frame(self.root, bg="#1e1e1e")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # === LEFT SIDE - QUIZ ===
        left_frame = tk.Frame(main_frame, bg="#1e1e1e")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Strike counter and Timer
        top_frame = tk.Frame(left_frame, bg="#1e1e1e")
        top_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Strike counter
        strike_frame = tk.Frame(top_frame, bg="#2e2e2e", relief="raised", bd=2)
        strike_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        self.strike_label = tk.Label(strike_frame, text="STRIKES: 0/3", 
                                   font=("Helvetica", 12, "bold"), fg="green", bg="#2e2e2e")
        self.strike_label.pack(pady=8)
        
        # Timer
        timer_frame = tk.Frame(top_frame, bg="#2e2e2e", relief="raised", bd=2)
        timer_frame.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(5, 0))
        
        self.timer_label = tk.Label(timer_frame, text="TIME: 15s", 
                                  font=("Helvetica", 12, "bold"), fg="white", bg="#2e2e2e")
        self.timer_label.pack(pady=8)
        
        # Question area
        question_frame = tk.Frame(left_frame, bg="#2e2e2e", relief="sunken", bd=2)
        question_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.question_label = tk.Label(question_frame, text="", font=("Helvetica", 12), 
                                     wraplength=500, justify="left", fg="white", bg="#2e2e2e")
        self.question_label.pack(padx=15, pady=15, anchor="w")
        
        # Options
        options_frame = tk.Frame(left_frame, bg="#1e1e1e")
        options_frame.pack(fill=tk.X, pady=10)
        
        self.radio_buttons = []
        for i in range(4):
            rb_frame = tk.Frame(options_frame, bg="#1e1e1e")
            rb_frame.pack(fill=tk.X, pady=3)
            
            rb = tk.Radiobutton(rb_frame, text="", variable=self.selected_option, 
                              value=i+1, font=("Helvetica", 11), 
                              fg="white", bg="#1e1e1e", selectcolor="#2e2e2e")
            rb.pack(side=tk.LEFT)
            
            option_text = tk.Label(rb_frame, text="", font=("Helvetica", 11), 
                                 fg="white", bg="#1e1e1e", anchor="w")
            option_text.pack(side=tk.LEFT, fill=tk.X, expand=True)
            self.radio_buttons.append(option_text)
        
        # Navigation
        nav_frame = tk.Frame(left_frame, bg="#1e1e1e")
        nav_frame.pack(fill=tk.X, pady=20)
        
        self.prev_button = tk.Button(nav_frame, text="← Previous", font=("Helvetica", 11),
                                   state="disabled", command=self.previous_question)
        self.prev_button.pack(side=tk.LEFT, padx=5)
        
        self.next_button = tk.Button(nav_frame, text="Next →", font=("Helvetica", 11),
                                   command=self.next_question)
        self.next_button.pack(side=tk.LEFT, padx=5)
        
        self.submit_button = tk.Button(nav_frame, text="Submit Quiz", font=("Helvetica", 11, "bold"),
                                     bg="#388e3c", fg="white", state="disabled",
                                     command=self.submit_quiz)
        self.submit_button.pack(side=tk.RIGHT, padx=5)
        
        # === RIGHT SIDE - PROCTORING ===
        right_frame = tk.Frame(main_frame, bg="#1e1e1e", width=350)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0))
        right_frame.pack_propagate(False)
        
        # Camera feed
        camera_frame = tk.Frame(right_frame, bg="#2e2e2e", relief="sunken", bd=2, height=220)
        camera_frame.pack(fill=tk.X, pady=(0, 10))
        camera_frame.pack_propagate(False)
        
        tk.Label(camera_frame, text="LIVE CAMERA FEED", font=("Helvetica", 12, "bold"), 
                fg="white", bg="#2e2e2e").pack(pady=8)
        
        self.camera_label = tk.Label(camera_frame, bg="black", text="Initializing camera...")
        self.camera_label.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Cheat probability graph
        graph_frame = tk.Frame(right_frame, bg="#2e2e2e", relief="sunken", bd=2)
        graph_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        tk.Label(graph_frame, text="CHEAT PROBABILITY", font=("Helvetica", 12, "bold"), 
                fg="white", bg="#2e2e2e").pack(pady=8)
        
        # Matplotlib graph
        self.fig, self.ax = plt.subplots(figsize=(4, 3), facecolor='#2e2e2e')
        self.ax.set_facecolor('#1e1e1e')
        self.ax.set_xlim(0, 50)
        self.ax.set_ylim(0, 1)
        self.ax.set_xlabel("Time", color='white', fontsize=8)
        self.ax.set_ylabel("Probability", color='white', fontsize=8)
        self.ax.tick_params(colors='white', labelsize=7)
        self.ax.set_title("Real-time Monitoring", color='white', fontsize=10)
        
        # Add threshold line
        self.ax.axhline(y=0.6, color='red', linestyle='--', alpha=0.7, linewidth=1)
        self.ax.text(25, 0.65, 'Warning Threshold', color='red', fontsize=7, ha='center')
        
        self.graph_line, = self.ax.plot([], [], 'cyan', linewidth=2)
        self.graph_canvas = FigureCanvasTkAgg(self.fig, graph_frame)
        self.graph_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def start_timer(self):
        """Start the 15-second timer for current question"""
        self.time_left = 15
        self.timer_running = True
        self.update_timer()

    def stop_timer(self):
        """Stop the current timer"""
        self.timer_running = False
        if self.timer_id:
            self.root.after_cancel(self.timer_id)

    def update_timer(self):
        """Update the timer display"""
        if self.timer_running and self.time_left > 0:
            # Update timer display with color coding
            if self.time_left <= 5:
                self.timer_label.config(text=f"TIME: {self.time_left}s", fg="red")
            elif self.time_left <= 10:
                self.timer_label.config(text=f"TIME: {self.time_left}s", fg="orange")
            else:
                self.timer_label.config(text=f"TIME: {self.time_left}s", fg="white")
            
            self.time_left -= 1
            self.timer_id = self.root.after(1000, self.update_timer)
        elif self.timer_running and self.time_left <= 0:
            # Time's up - auto move to next question
            self.time_up()

    def time_up(self):
        """Handle when time runs out for a question"""
        self.stop_timer()
        messagebox.showwarning("Time's Up!", "Time is up for this question! Moving to next question.")
        
        # Save current answer (if any) and move to next question
        self.user_answers[self.index] = self.selected_option.get()
        
        if self.index < len(self.questions) - 1:
            self.index += 1
            self.display_question()
        else:
            # Last question - submit quiz
            self.submit_quiz()

    def display_question(self):
        if self.index < len(self.questions):
            q = self.questions[self.index]
            self.question_label.config(text=f"Q{self.index+1}/{len(self.questions)}: {q[1]}")
            
            for i in range(4):
                self.radio_buttons[i].config(text=q[i+2])
            
            self.selected_option.set(self.user_answers[self.index])
            
            self.prev_button.config(state="normal" if self.index > 0 else "disabled")
            self.next_button.config(state="normal" if self.index < len(self.questions)-1 else "disabled")
            self.submit_button.config(state="normal" if self.index == len(self.questions)-1 else "disabled")
            
            # Start timer for this question
            self.start_timer()

    def previous_question(self):
        self.stop_timer()
        self.user_answers[self.index] = self.selected_option.get()
        self.index -= 1
        self.display_question()

    def next_question(self):
        self.stop_timer()
        self.user_answers[self.index] = self.selected_option.get()
        self.index += 1
        self.display_question()

    def submit_quiz(self):
        self.stop_timer()
        self.proctor.stop_monitoring()
        self.user_answers[self.index] = self.selected_option.get()
        
        # Calculate score
        self.score = 0
        for i, q in enumerate(self.questions):
            if self.user_answers[i] == q[6]:
                self.score += 1
        
        # Check strikes
        if self.proctor.strikes >= self.proctor.max_strikes:
            final_score = 0
            message = "❌ Quiz terminated! Zero score due to suspicious behavior."
        else:
            final_score = self.score
            message = f"✅ Quiz completed! Score: {self.score}/{len(self.questions)}"
        
        save_result(self.username, final_score)
        messagebox.showinfo("Quiz Completed", message)
        self.root.destroy()

    def monitor_strikes(self):
        if self.proctor.monitoring_active:
            # Update strike display
            self.strike_label.config(text=f"STRIKES: {self.proctor.strikes}/3")
            
            # Update color based on strikes
            if self.proctor.strikes == 1:
                self.strike_label.config(fg="orange")
            elif self.proctor.strikes == 2:
                self.strike_label.config(fg="red")
            elif self.proctor.strikes >= 3:
                self.strike_label.config(text="STRIKES: 3/3 - TERMINATED", fg="red")
                self.terminate_quiz()
                return
            
            self.root.after(1000, self.monitor_strikes)

    def terminate_quiz(self):
        self.stop_timer()
        self.proctor.stop_monitoring()
        save_result(self.username, 0)
        messagebox.showerror("Quiz Terminated", 
                           "Quiz terminated! Your face was not visible to the camera.\nScore: 0")
        self.root.destroy()

    def update_camera_display(self):
        """Update the camera feed in the right panel"""
        if self.proctor.monitoring_active:
            frame = self.proctor.get_camera_frame()
            if frame is not None:
                # Convert to PhotoImage
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                self.camera_label.imgtk = imgtk
                self.camera_label.configure(image=imgtk)
            else:
                self.camera_label.configure(text="Camera not available", fg="red")
            
            self.root.after(100, self.update_camera_display)  # Update every 100ms

    def update_graph(self):
        """Update the cheat probability graph"""
        if self.proctor.monitoring_active:
            try:
                # Update graph with current data
                x_data = list(range(50))
                self.graph_line.set_data(x_data, self.proctor.cheat_data)
                
                # Change graph color based on cheat probability
                current_prob = self.proctor.cheat_probability
                if current_prob > 0.6:
                    self.graph_line.set_color('red')
                elif current_prob > 0.3:
                    self.graph_line.set_color('orange')
                else:
                    self.graph_line.set_color('cyan')
                
                self.graph_canvas.draw_idle()
            except Exception as e:
                print(f"Graph update error: {e}")
            
            self.root.after(500, self.update_graph)  # Update every 500ms

# --- Run App ---
if __name__ == "__main__":
    username = sys.argv[1] if len(sys.argv) > 1 else "student"
    root = tk.Tk()
    app = QuizApp(root, username)
    root.mainloop()