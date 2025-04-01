import os

class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    KNOWN_FACES_FOLDER = os.path.join(BASE_DIR, 'known_faces')
    SECRET_KEY = 'your-secret-key-here'

    # Email configuration for Flask-Mail
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'gamagdamir@gmail.com'  # Replace with your Gmail address
    MAIL_PASSWORD = 'evvp gnjl sxkw nhun'   # Replace with your Gmail App Password
    MAIL_DEFAULT_SENDER = MAIL_USERNAME  # **Add this line**
