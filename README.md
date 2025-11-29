Exam Management System with AI Proctoring
🎓 Project for JIIT
Requirements
Python 3.8+

MySQL Server

OpenCV for computer vision

Webcam for proctoring functionality

Project Description
The Exam Management System with AI Proctoring is a comprehensive online assessment platform developed as a DBMS project. It addresses the critical need for maintaining academic integrity in remote examinations by replacing traditional manual invigilation with automated AI-powered monitoring.

The system manages students, teachers, questions, and exam results through a structured MySQL database, eliminating the inefficiencies of paper-based exams and manual supervision. It ensures fair assessment through real-time behavioral monitoring and prevents malpractices during online tests.

🗄️ Database Design
The project implements a normalized schema with core tables:

Users - Stores student and teacher credentials with role-based access

Questions - Manages quiz questions with multiple-choice options and correct answers

Quiz_Results - Tracks student performance and scores

Service tables - Supports the proctoring system's monitoring data

The schema maintains data integrity through appropriate relationships and constraints, preventing duplication and ensuring consistent assessment records.

🔧 Core Functionality
For Students:
Secure Authentication with role-based access

Timed Assessments with automatic submission

Real-time Proctoring via webcam monitoring

Performance Tracking with historical results

Profile Management for personal information updates

For Teachers:
Question Bank Management - CRUD operations for exam questions

Student Management - Registration and profile oversight

Results Analytics - Performance monitoring and reporting

Proctoring Oversight - Real-time cheating detection alerts

AI Proctoring Features:
Face Detection - Ensures test-taker presence

Head Pose Analysis - Detects suspicious movements

Strike System - Progressive warnings for violations

Automatic Termination - Quiz cancellation upon threshold breach

Live Monitoring - Real-time camera feed and behavioral analytics

💻 Technical Implementation
The backend is implemented in Python with:

Tkinter for the graphical user interface

PyMySQL for database connectivity

OpenCV for computer vision and face detection

Matplotlib for real-time monitoring visualizations

The system demonstrates complex database operations including:

CRUD operations for user and question management

Join queries for result analysis and reporting

Transaction management for data consistency

Real-time data processing for proctoring analytics

📊 Key Advantages
Automated Integrity: Replaces manual invigilation with AI monitoring

Scalable Architecture: Supports multiple concurrent examinations

Comprehensive Reporting: Detailed analytics for performance assessment

User-friendly Interface: Intuitive design for both students and faculty

Data Security: Protected authentication and role-based access control

This repository contains complete Python source code, database schema design, ER diagrams, and implementation scripts for a robust, production-ready online examination system with integrated academic integrity protection.
