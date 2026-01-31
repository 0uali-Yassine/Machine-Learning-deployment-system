import cv2
import mediapipe as mp

# Initialiser les solutions MediaPipe
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

# Initialiser la webcam
cap = cv2.VideoCapture(0)

# Utiliser le modèle de détection
with mp_face_detection.FaceDetection(
    model_selection=0, min_detection_confidence=0.5) as face_detection:
    
    print("Appuyez sur 'q' pour quitter.")

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            break

        # Convertir l'image de BGR à RGB (MediaPipe utilise le RGB)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_detection.process(image_rgb)

        # Dessiner les détections sur l'image originale
        if results.detections:
            for detection in results.detections:
                # Dessine le carré et les points clés (yeux, nez, oreilles, bouche)
                mp_drawing.draw_detection(image, detection)

        # Affichage
        cv2.imshow('Detection de Visage - MediaPipe', image)

        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()