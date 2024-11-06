from flask import Flask, render_template, request
import time
import threading
import os
import cv2
import numpy as np
import faceRecognition as fr  # Assuming you have a faceRecognition module

app = Flask(__name__)

# Load the LBPH face recognizer and read the training data
face_recognizer = cv2.face_LBPHFaceRecognizer.create()
face_recognizer.read("C:\\Users\\poona\\Downloads\\Two Factor Authentication\\templates\\trainingData.yml")  # Load saved training data

# Dictionary mapping label to name
name = {0: "Aditya", 1: "Vasu", 2: "Riya"}

# Route for the index page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/second')
def second():
    return render_template('index1.html')

verified = False

def verify_face():
    global verified
    cap = cv2.VideoCapture(0)
    start_time = time.time() 
    count = 1

    # Ensure folder existence
    if not os.path.exists("C:\\Users\\poona\\Downloads\\Two Factor Authentication\\templates\\images"):
        os.makedirs("C:\\Users\\poona\\Downloads\\Two Factor Authentication\\templates\\images")

    while not verified and time.time() - start_time < 10:
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
            if confidence < 75:  # Adjust threshold as needed
                predicted_name = name[label]
                fr.put_text(frame, predicted_name, x, y)
                # If the predicted name is printed, set verified to True and break out of the loop
                if predicted_name:
                    verified = True
                    break

        # Display the frame with face detection and recognition information
        cv2.imshow('Face Recognition', frame)

        # Break the loop if 'q' key is pressed or if verified is True
        if cv2.waitKey(1) & 0xFF == ord('q') or verified:
            break

    # Save the image with status (whether verified or not) and a unique filename
    status = "Verified" if verified else "Not_Verified"
    filename = f"C:\\Users\\poona\\Downloads\\Two Factor Authentication\\templates\\images\\{status}_{count}.jpg"
    while os.path.exists(filename):  # Ensure filename uniqueness
        count += 1
        filename = f"C:\\Users\\poona\\Downloads\\Two Factor Authentication\\templates\\images\\{status}_{count}.jpg"
    cv2.imwrite(filename, frame)

    cap.release()
    cv2.destroyAllWindows()

def timeout():
    global verified
    time.sleep(10)  # Wait for 10 seconds
    if not verified:
        verified = False # If not verified during timeout, set verified to True

# New route for handling face verification request
@app.route('/verify_face', methods=['GET'])
def verify_face_route():
    global verified
    verified = False  # Reset verification flag

    # Start face verification in a separate thread
    verification_thread = threading.Thread(target=verify_face)
    verification_thread.start()

    # Start timeout in a separate thread
    timeout_thread = threading.Thread(target=timeout)
    timeout_thread.start()

    # Wait for face verification to finish
    verification_thread.join()

    if verified:
        return "Face Verified"
    else:
        return "Not Verified"

@app.route('/third')
def third():
    return render_template('index2.html')

if __name__ == "__main__":
    app.run(debug=True)