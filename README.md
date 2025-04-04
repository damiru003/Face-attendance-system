# Attend AI - Intelligent Attendance System

**Attend AI** is an intelligent attendance system that automates attendance tracking in educational settings using AI and computer vision. It leverages facial recognition, liveness detection, and emotion analysis to identify students, prevent spoofing, and assess engagement levels. Built with Flask, OpenCV, and advanced AI libraries, Attend AI offers a web-based interface for student registration, attendance marking, and record viewing, with features like email notifications and a responsive dashboard.

---

## Features
- **Student Registration**: Register students with facial images and details, stored in a CSV file.
- **Real-Time Attendance Marking**: Identify students using facial recognition, verify liveness, and detect emotions.
- **Emotion Analysis**: Assess student engagement with emotion-based scoring (e.g., 90% for "happy").
- **Dashboard**: View attendance records, summary statistics, and filter records by name or date.
- **Email Notifications**: Send confirmation emails to students upon registration.
- **Responsive Design**: A modern, dark-themed interface usable on desktop and mobile devices.

---

## Prerequisites
Before running Attend AI, ensure you have:
- **Python 3.8 or higher**: [Download Python](https://www.python.org/downloads/)
- **pip**: Python package manager (comes with Python)
- **Git**: For cloning the repository [Download Git](https://git-scm.com/downloads)
- **A webcam**: For capturing images during registration and attendance marking.
- **An email server configuration**: For sending email notifications (e.g., Gmail SMTP).
- A system with at least 4GB of RAM and a decent CPU (e.g., Intel i3 or equivalent).

---

## How to Run the System

### 1. Clone the Repository
Clone the project to your local machine:
```bash
git clone https://github.com/[YOUR-USERNAME]/attend-ai.git
cd attend-ai
```

### 2. Set Up a Virtual Environment (Recommended)
Create and activate a virtual environment to isolate dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
Install the required Python packages listed in `requirements.txt`:
```bash
pip install -r requirements.txt
```
The `requirements.txt` file includes:
```
flask==2.0.1
opencv-python==4.5.5.64
face_recognition==1.3.0
deepface==0.0.75
flask-mail==0.9.1
numpy==1.21.0
```
**Note**: `face_recognition` requires `dlib`, which may need additional setup (see [Troubleshooting](#troubleshooting)).

### 4. Configure Email Settings
Set up email notifications by configuring your email server in `config.py` (create the file if it doesn't exist):
```python
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = '[YOUR-EMAIL]@gmail.com'
MAIL_PASSWORD = '[YOUR-APP-PASSWORD]'  # Use an App Password if using Gmail
MAIL_DEFAULT_SENDER = '[YOUR-EMAIL]@gmail.com'
```
- For Gmail, generate an App Password (Google Account > Security > 2-Step Verification > App Passwords).

### 5. Run the Application Locally
Start the Flask application:
```bash
python app.py
```
The application will run on `http://127.0.0.1:5000`.

### 6. Access the Application Locally
- Open a web browser and go to `http://127.0.0.1:5000`.
- You'll see the homepage with options to register students, mark attendance, and view the dashboard.

### 7. Access on Other Devices (Optional)
To access Attend AI from other devices on the same network (e.g., a smartphone):
1. **Find Your Local IP Address**:
   - Windows: Run `ipconfig` in Command Prompt and look for `IPv4 Address` (e.g., `192.168.1.100`).
   - macOS/Linux: Run `ifconfig` or `ip addr` and look for `inet` (e.g., `192.168.1.100`).
2. **Run the Flask Application with External Access**:
   ```bash
   python app.py --host=0.0.0.0 --port=5000
   ```
   Or modify `app.py`:
   ```python
   if __name__ == '__main__':
       app.run(host='0.0.0.0', port=5000, debug=True)
   ```
   Then run:
   ```bash
   python app.py
   ```
3. **Access from Another Device**:
   - Ensure the device is on the same Wi-Fi network.
   - Open a browser and go to `http://[YOUR-LOCAL-IP]:5000` (e.g., `http://192.168.1.100:5000`).

### 8. View the Output
- **Homepage**: `http://[YOUR-LOCAL-IP]:5000/` - Displays a real-time clock and links to core features.
- **Student Registration**: `/register` - Capture a student's image and enter details; a confirmation email is sent.
- **Attendance Marking**: `/take_attendance` - Start the camera to mark attendance with real-time recognition and emotion detection.
- **Dashboard**: `/dashboard` - View attendance records, summary stats (total students, present today), and filter records.
- **Email Notifications**: Check the student's email for a styled confirmation email.
- **CSV Files**: View raw data in `data/students.csv` (student details) and `data/attendance.csv` (attendance records).

---

## Troubleshooting
- **Camera Not Working**:
  - Ensure your webcam is connected and not in use by another application.
  - Use `/stop_camera` (e.g., `http://127.0.0.1:5000/stop_camera`) to release the camera.
  - Verify OpenCV: `pip install opencv-python`.
- **Error Installing `face_recognition`**:
  - Install `dlib` dependencies:
    ```bash
    # macOS
    brew install cmake
    brew install libopenblas
    # Ubuntu
    sudo apt-get install build-essential cmake libopenblas-dev
    ```
  - Reinstall: `pip install face_recognition`.
- **Email Not Sending**:
  - Check `config.py` for correct email settings.
  - Use an App Password for Gmail.
- **Not Accessible on Other Devices**:
  - Ensure `host=0.0.0.0` and port 5000 is open in your firewall:
    ```bash
    sudo ufw allow 5000  # On macOS/Linux
    ```
  - Confirm devices are on the same network.

---

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
