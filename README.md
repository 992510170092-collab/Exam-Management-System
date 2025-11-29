EXAM MANAGEMENT SYSTEM WITH AI PROCTORING

This is the DBMS project for JIIT

1. PROJECT OVERVIEW

1.1 Introduction
The Exam Management System with AI Proctoring is a comprehensive online assessment platform designed to maintain academic integrity in remote examinations. This system replaces traditional manual invigilation with automated AI-powered monitoring, ensuring fair and secure assessments.

1.2 Project Scope
- Automated online examination platform
- AI-based proctoring system
- Role-based access for students and teachers
- Real-time monitoring and cheating detection
- Comprehensive result management

1.3 Technologies Used
- Frontend: Python Tkinter
- Backend: Python
- Database: MySQL
- Computer Vision: OpenCV
- Data Visualization: Matplotlib
- Image Processing: PIL/Pillow

2. SYSTEM ARCHITECTURE

2.1 System Flow
Login System → Role-based Access → 
Student Dashboard (Take Quiz/View Results) 
Teacher Dashboard (Manage Questions/Students)

2.2 Database Schema

2.2.1 Tables Structure

USERS Table:

<img width="601" height="259" alt="image" src="https://github.com/user-attachments/assets/09494821-5c04-409a-bd8b-26d3a8314035" />


QUESTIONS Table:

<img width="645" height="280" alt="image" src="https://github.com/user-attachments/assets/a5d77a33-a411-4541-9b4a-fbc1b75a07fb" />

QUIZ_RESULTS Table:

<img width="556" height="195" alt="image" src="https://github.com/user-attachments/assets/a2a2a09c-eb2d-47f2-a0d7-f751af2c13b1" />

3. MODULE DESCRIPTION

3.1 Authentication Module (login.py)
- Handles user authentication
- Role-based access control
- Secure password management
- Session management

Key Functions:
- verify_login(username, password, role)
- Role validation (student/teacher)

3.2 Student Module (student.py)
- Quiz interface
- Result viewing
- Profile management
- Navigation to proctored exams

Key Features:
- Take Quiz: Launches proctored examination
- View Results: Historical performance
- Edit Profile: Password updates
- Logout: Secure session termination

3.3 Teacher Module (teacher.py)
- Question bank management
- Student management
- Results monitoring
- Administrative controls

Key Features:
- Add/Edit/Delete questions
- Student registration
- Performance analytics
- Bulk operations

3.4 Quiz Module (quiz.py)
- Main examination interface
- Timer management
- Question navigation
- Answer submission

Key Components:
- 15-second per question timer
- Previous/Next navigation
- Real-time progress tracking
- Auto-submission on timeout

3.5 Proctoring Module

3.5.1 Head Pose Detection (head_pose.py)
- Face detection using Haar cascades
- Head position tracking
- Suspicious movement detection
- Real-time coordinate tracking

3.5.2 Cheat Detection (detection.py)
- Behavioral analysis
- Probability-based cheating detection
- Threshold monitoring
- Strike system implementation

4. AI PROCOTING SYSTEM

4.1 Face Detection
- Uses OpenCV Haar cascades
- Real-time webcam feed processing
- Continuous presence monitoring
- Frame-by-frame analysis

4.2 Behavioral Monitoring
- Head pose analysis (X and Y axis)
- Eye contact tracking
- Movement pattern detection
- Attention span monitoring

4.3 Strike System
- 3-strike policy for violations
- Progressive warnings
- Automatic quiz termination
- Real-time notification

4.4 Cheat Probability Algorithm
- Continuous probability calculation (0.0 to 1.0)
- Threshold-based alerts (0.6 for warning)
- Real-time graph visualization
- Historical data tracking

5. INSTALLATION GUIDE

5.1 Prerequisites
- Python 3.8 or higher
- MySQL Server 8.0+
- Webcam
- Internet connection

5.2 Required Python Packages
