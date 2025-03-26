import os
import csv
import logging
from config import Config
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

DATA_DIR = Config.DATA_DIR
STUDENTS_CSV = os.path.join(DATA_DIR, 'students.csv')
ATTENDANCE_CSV = os.path.join(DATA_DIR, 'attendance.csv')

def init_storage():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        logger.debug(f"Data directory created at {DATA_DIR}")
    else:
        logger.debug(f"Data directory already exists at {DATA_DIR}")

    if not os.path.exists(STUDENTS_CSV):
        with open(STUDENTS_CSV, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['student_id', 'first_name', 'last_name', 'image_path'])
        logger.debug(f"students.csv initialized at {STUDENTS_CSV}")
    else:
        logger.debug(f"students.csv already exists at {STUDENTS_CSV}")

    if not os.path.exists(ATTENDANCE_CSV):
        with open(ATTENDANCE_CSV, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'student_name', 'time', 'emotion', 'student_id'])
        logger.debug(f"attendance.csv initialized at {ATTENDANCE_CSV}")
    else:
        logger.debug(f"attendance.csv already exists at {ATTENDANCE_CSV}")

def register_student(student_id, first_name, last_name):
    # Ensure the CSV file exists
    if not os.path.exists(STUDENTS_CSV):
        logger.error(f"students.csv does not exist at {STUDENTS_CSV}. Initializing it now.")
        init_storage()  # Reinitialize storage to create the file

    # Check for duplicates
    try:
        with open(STUDENTS_CSV, 'r', newline='') as f:
            reader = csv.reader(f)
            header = next(reader, None)  # Safely get the header
            if not header:
                logger.warning(f"students.csv at {STUDENTS_CSV} is empty. Reinitializing.")
                init_storage()
                with open(STUDENTS_CSV, 'r', newline='') as f:
                    reader = csv.reader(f)
                    next(reader)  # Skip the newly created header

            for row in reader:
                if len(row) < 4:  # Ensure the row has all expected columns
                    logger.warning(f"Skipping malformed row in students.csv: {row}")
                    continue
                if row[0] == student_id:
                    raise Exception(f"Student ID {student_id} already registered!")
                if row[1] == first_name and row[2] == last_name:
                    raise Exception(f"Student name {first_name} {last_name} already registered!")
    except Exception as e:
        logger.error(f"Error reading students.csv: {str(e)}")
        raise

    # Write the new student to the CSV
    try:
        with open(STUDENTS_CSV, 'a', newline='') as f:
            writer = csv.writer(f)
            image_path = os.path.join(Config.KNOWN_FACES_FOLDER, f"{first_name}_{last_name}.jpg")
            writer.writerow([student_id, first_name, last_name, image_path])
            logger.debug(f"Registered student: {first_name} {last_name} (ID: {student_id}) with image path {image_path}")
    except Exception as e:
        logger.error(f"Error writing to students.csv: {str(e)}")
        raise Exception(f"Failed to register student: {str(e)}")

def log_attendance(student_name, emotion):
    if not student_name:
        logger.error("Student name is empty; cannot log attendance.")
        return
    
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    first_name, last_name = student_name.split('_')
    student_id = "Unknown"
    with open(STUDENTS_CSV, 'r', newline='') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if row[1] == first_name and row[2] == last_name:
                student_id = row[0]
                break

    with open(ATTENDANCE_CSV, 'r', newline='') as f:
        reader = csv.reader(f)
        rows = list(reader)
        next_id = len(rows)

    with open(ATTENDANCE_CSV, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([next_id, student_name, time_now, emotion, student_id])
        logger.debug(f"Attendance logged for {student_name} (ID: {student_id}) at {time_now}")

def get_attendance_records():
    records = []
    with open(ATTENDANCE_CSV, 'r', newline='') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        if not header:
            logger.debug("attendance.csv is empty.")
            return records
        for row in reader:
            if len(row) < 5:
                logger.warning(f"Skipping malformed row in attendance.csv: {row}")
                continue
            records.append({
                'id': row[0],
                'student_name': row[1],
                'time': row[2],
                'emotion': row[3],
                'student_id': row[4]
            })
    logger.debug(f"Retrieved {len(records)} attendance records.")
    return records