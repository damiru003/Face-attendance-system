import os

class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # Root directory of the project
    DATA_DIR = os.path.join(BASE_DIR, 'data')  # Directory for CSV files
    KNOWN_FACES_FOLDER = os.path.join(BASE_DIR, 'known_faces')  # Directory for face images
    SECRET_KEY = 'your-secret-key-here'  # Secret key for Flask