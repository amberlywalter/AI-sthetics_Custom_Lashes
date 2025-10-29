import cv2
import mediapipe as mp

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, refine_landmarks=True)

def detect_face_landmarks(image_path):
    image = cv2.imread(image_path)
    if image is None:
        return None, "Image not found"
    
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)
    if not results.multi_face_landmarks:
        return None, "No face detected"
    return results.multi_face_landmarks[0], None
