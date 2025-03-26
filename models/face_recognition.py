import face_recognition
import os
import cv2
from config import Config
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

known_face_encodings = []
known_face_names = []

def load_known_faces():
    global known_face_encodings, known_face_names
    known_face_encodings.clear()
    known_face_names.clear()

    for filename in os.listdir(Config.KNOWN_FACES_FOLDER):
        if filename.endswith(('.jpg', '.png')):
            image_path = os.path.join(Config.KNOWN_FACES_FOLDER, filename)
            image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(image)
            if encodings:
                name = filename.split('.')[0]
                if '_' in name:
                    name = name.replace(' ', '')
                    known_face_encodings.append(encodings[0])
                    known_face_names.append(name)
                    logger.debug(f"Loaded face: {name} from {image_path}")
                else:
                    logger.warning(f"Skipping {image_path}: Name '{name}' does not contain an underscore (expected format: first_name_last_name)")
            else:
                logger.warning(f"No face encodings found in {image_path}")
    logger.debug(f"Total faces loaded: {len(known_face_names)}")

def recognize_faces(frame):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
    
    recognized = []
    seen_names = set()
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.6)
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]
            if name not in seen_names:
                recognized.append((name, (top, right, bottom, left)))
                seen_names.add(name)
                logger.debug(f"Recognized {name} (Tolerance: 0.6)")
        else:
            logger.debug("No match found for face encoding.")
    if not recognized:
        logger.debug("No faces recognized in this frame.")
    return recognized

def check_liveness(frame):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    if face_locations:
        landmarks = face_recognition.face_landmarks(rgb_frame, face_locations)
        for landmark in landmarks:
            left_eye = landmark.get('left_eye', [])
            right_eye = landmark.get('right_eye', [])
            if len(left_eye) > 0 and len(right_eye) > 0:
                return True
    return False