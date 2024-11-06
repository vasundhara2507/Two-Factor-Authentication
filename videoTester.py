# This code will be moved to a separate Python script (let's call it videoTester.py)
import os
import cv2
import numpy as np
import faceRecognition as fr  # Assuming you have a faceRecognition module

# Load the LBPH face recognizer and read the training data
face_recognizer = cv2.face_LBPHFaceRecognizer.create()
face_recognizer.read("C:\\Users\\poona\\Downloads\\Two Factor Authentication\\templates\\trainingData.yml")  # Load saved training data

# Dictionary mapping label to name
name = {0: "Aditya", 1: "Vasu"}

def verify_face():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()  # Capture frame from the camera

        # Perform face detection
        faces_detected, gray_img = fr.faceDetection(frame)

        # Iterate through detected faces for recognition
        for face in faces_detected:
            (x, y, w, h) = face
            roi_gray = cv2.resize(gray_img[y:y + h, x:x + w], (100, 100))  # Resize for consistency
            label, confidence = face_recognizer.predict(roi_gray)  # Predict label and confidence
            print("Confidence:", confidence)
            print("Label:", label)
            fr.draw_rect(frame, face)

            # If confidence is below a threshold, recognize the face
            if confidence < 70:  # Adjust threshold as needed
                predicted_name = name[label]
                fr.put_text(frame, predicted_name, x, y)

        # Display the frame with face detection and recognition information
        cv2.imshow('Face Recognition', frame)

        # Break the loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    verify_face()
