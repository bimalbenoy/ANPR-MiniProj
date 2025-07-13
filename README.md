# 🚗 Automatic Number Plate Recognition (ANPR)

This project implements an *Automatic Number Plate Recognition (ANPR)* system using computer vision and deep learning techniques. It detects vehicle number plates in real-time, extracts plate numbers using OCR and logs them into a Django web application for access control and monitoring.

---

## 📦 Tech Stack

- 🔍 YOLOv8 for license plate detection
- 📖 PaddleOCR for number plate text recognition
- 🎥 OpenCV for image & video processing
- 🌐 Django (Python) for the web application
- 💾 SQLite for the backend database

---

## 🗂 Project Structure

anpr-project/
├── basic/ # Django app: handles detection and logic
├── home/ # Django app: likely homepage/views
├── media/ # Folder for uploaded media files
├── templates/ # HTML templates (Django views)
│ ├── registration/
│ │ ├── login.html
│ │ ├── register.html
│ │ └── logged_out.html
│ ├── home.html
│ ├── contact.html
│ ├── search.html
│ ├── layout.html
│ └── layout1.html
├── uploads/ # Image/video uploads for detection
├── db.sqlite3 # SQLite database
├── manage.py # Django project runner
└── requirements.txt # Python dependencies

---

## 🚀 Features

- Real-time vehicle number plate detection (YOLOv8)
- OCR-based text recognition (PaddleOCR)
- Auto-logging of recognized numbers
- Resident vs Visitor vs Criminal classification logic
- Login & registration system for guards/admins
- Plate search and view history functionality

## 🔧 Installation Instructions

### 1. Clone the Repository

bash
https://github.com/AmishaShaney/number-plate-recognition.git
cd number-plate-recognition


### 2. Create & Activate Virtual Environment

bash
python -m venv .venv
.\.venv\Scripts\activate     # For Windows PowerShell
# OR
source .venv/bin/activate    # For macOS/Linux


### 3. Install Dependencies

bash
pip install -r requirements.txt



### 4.Run the Server

bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver


---
### 🌐 Usage
Go to http://127.0.0.1:8000/

Login or Register via registration/login.html

Upload an image or video in the UI (e.g., uploads/)

The system will:

Detect the plate using YOLOv8

Extract number using PaddleOCR

Save and display the result

---
### 🧑‍💻 Team
Amisha Shaney

Bimal Benoy

Eldho G Peter

Fida K A

Dept. of Computer Science,
Model Engineering College, Kochi
March 2025
