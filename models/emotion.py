from deepface import DeepFace

def detect_emotion(face_img):
    try:
        result = DeepFace.analyze(face_img, actions=['emotion'], enforce_detection=False)
        return result[0]['dominant_emotion']
    except:
        return "Unknown"