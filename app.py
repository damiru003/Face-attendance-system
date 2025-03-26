from flask import Flask, render_template, Response, request, redirect, url_for, flash
from config import Config
from models.face_recognition import recognize_faces, load_known_faces, check_liveness
from models.emotion import detect_emotion
from utils.storage import init_storage, register_student, log_attendance, get_attendance_records
import cv2
import os
import numpy as np
import time
import logging
import csv
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = app.config['SECRET_KEY']

# Ensure the known_faces directory exists before loading faces
if not os.path.exists(app.config['KNOWN_FACES_FOLDER']):
    os.makedirs(app.config['KNOWN_FACES_FOLDER'])
    logger.debug(f"Created known_faces directory at {app.config['KNOWN_FACES_FOLDER']}")

# Initialize CSV storage and load known faces
init_storage()
load_known_faces()

# Global variables
latest_frame = None
last_detection_time = {}
detection_cooldown = 5
cap = None

def gen_frames_register():
    global latest_frame, cap
    try:
        logger.debug("Attempting to open camera for registration")
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            logger.error("Camera not accessible for registration")
            raise Exception("Camera not accessible")
        logger.debug("Camera opened successfully for registration")
        while True:
            success, frame = cap.read()
            if not success:
                logger.error("Failed to read frame from camera in registration")
                break
            latest_frame = frame.copy()
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    except Exception as e:
        logger.error(f"Error in gen_frames_register: {str(e)}")
    finally:
        if cap is not None:
            cap.release()
            cap = None
            logger.debug("Camera released in gen_frames_register")

def gen_frames_attendance():
    global latest_frame, last_detection_time, cap
    try:
        logger.debug("Attempting to open camera for attendance")
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            logger.error("Camera not accessible for attendance")
            raise Exception("Camera not accessible")
        logger.debug("Camera opened successfully for attendance")
        message = "Scanning..."
        recognized_names = set()
        while True:
            success, frame = cap.read()
            if not success:
                logger.error("Failed to read frame from camera in attendance")
                break
            latest_frame = frame.copy()
            current_time = time.time()

            recognized_faces = recognize_faces(frame)
            if recognized_faces:
                for name, (top, right, bottom, left) in recognized_faces:
                    if name in recognized_names:
                        message = f"Attendance already recorded for {name} in this session"
                        continue

                    if name not in last_detection_time or (current_time - last_detection_time.get(name, 0) >= detection_cooldown):
                        if check_liveness(frame):
                            emotion = detect_emotion(frame[top:bottom, left:right])
                            engagement_score = {"happy": 90, "neutral": 70, "sad": 50, "angry": 30, "unknown": 0}.get(emotion.lower(), 50)
                            log_attendance(name, f"{emotion} (Engagement: {engagement_score}%)")
                            message = f"Attendance Recorded for {name}"
                            last_detection_time[name] = current_time
                            recognized_names.add(name)
                        else:
                            message = "Liveness Check Failed"

            for name, (top, right, bottom, left) in recognized_faces:
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, name, (left, top-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            cv2.putText(frame, message, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    except Exception as e:
        logger.error(f"Error in gen_frames_attendance: {str(e)}")
    finally:
        if cap is not None:
            cap.release()
            cap = None
            logger.debug("Camera released in gen_frames_attendance")

@app.route('/')
def index():
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template('index.html', current_datetime=current_datetime)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        student_id = request.form['student_id']
        if first_name and last_name and student_id and latest_frame is not None:
            try:
                name = f"{first_name}_{last_name}"
                filepath = os.path.join(app.config['KNOWN_FACES_FOLDER'], f"{name}.jpg")
                cv2.imwrite(filepath, latest_frame)
                register_student(student_id, first_name, last_name)
                load_known_faces()
                flash('Student registered successfully!', 'success')
            except Exception as e:
                flash(str(e), 'error')
                return redirect(url_for('register'))
        else:
            flash('Please fill in all fields and ensure the camera is capturing an image.', 'error')
        return redirect(url_for('register'))
    return render_template('register.html')

@app.route('/register_feed')
def register_feed():
    return Response(gen_frames_register(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/take_attendance')
def take_attendance():
    return render_template('take_attendance.html')

@app.route('/attendance_feed')
def attendance_feed():
    return Response(gen_frames_attendance(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/dashboard')
def dashboard():
    records = get_attendance_records()
    
    # Calculate summary data
    total_students = 0
    with open(os.path.join(Config.DATA_DIR, 'students.csv'), 'r', newline='') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        total_students = sum(1 for _ in reader)

    today = datetime.now().strftime("%Y-%m-%d")
    present_today = sum(1 for record in records if record['time'].startswith(today))
    
    attendance_rate = (present_today / total_students * 100) if total_students > 0 else 0
    attendance_rate = round(attendance_rate, 2)

    return render_template('dashboard.html', records=records, total_students=total_students, present_today=present_today, attendance_rate=attendance_rate)

@app.route('/stop_camera')
def stop_camera():
    global cap
    if cap is not None:
        cap.release()
        cap = None
        logger.debug("Camera released via stop_camera route")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)