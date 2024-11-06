import cv2
import os

# Function to adjust brightness and contrast of an image
def adjust_brightness_contrast(image, brightness=0, contrast=0):
    if brightness != 0:
        if brightness > 0:
            shadow = brightness
            highlight = 255
        else:
            shadow = 0
            highlight = 255 + brightness
        alpha_b = (highlight - shadow) / 255
        gamma_b = shadow

        buf = cv2.addWeighted(image, alpha_b, image, 0, gamma_b)

    else:
        buf = image.copy()

    if contrast != 0:
        f = 131 * (contrast + 127) / (127 * (131 - contrast))
        alpha_c = f
        gamma_c = 127 * (1 - f)

        buf = cv2.addWeighted(buf, alpha_c, buf, 0, gamma_c)

    return buf

# Function to capture images from different angles with varying brightness and contrast
def capture_images(output_dir, num_images_per_angle):
    # Initialize camera capture
    cap = cv2.VideoCapture(0)
    angle = 0  # Initial angle

    brightness_levels = range(50, -51, -1)  # From high to low brightness

    for brightness in brightness_levels:
        count = 0  # Initialize count for captured images

        while count < num_images_per_angle:
            ret, frame = cap.read()  # Capture frame-by-frame

            # Convert frame to grayscale for face detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Adjust brightness and contrast
            frame = adjust_brightness_contrast(frame, brightness=brightness, contrast=30)  # Adjust contrast here

            # Use a pre-trained face detection model to detect faces
            face_cascade = cv2.CascadeClassifier(
                'C:\\Users\\poona\\Downloads\\Two Factor Authentication\\templates\\HaarCascade\\haarcascade_frontalface_default.xml')

            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            for (x, y, w, h) in faces:
                # Draw rectangle around detected face
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

                # Capture images from the current angle
                filename = f"angle_{angle}brightness{brightness}image{count}.jpg"
                filepath = os.path.join(output_dir, filename)
                cv2.imwrite(filepath, frame[y:y+h, x:x+w])
                print(f"Image {count + 1} captured from angle {angle} with brightness {brightness}")
                count += 1

            # Display the captured frame with detected face
            cv2.imshow('Capture Images', frame)

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        angle += 1

    # Release the capture
    cap.release()
    cv2.destroyAllWindows()

# Path to store captured images
output_dir = "C:\\Users\\poona\\Downloads\\Two Factor Authentication\\templates\\trainingImages\\1"

# Number of images to capture from each angle
num_images_per_angle = 10

# Create directory to store captured images
os.makedirs(output_dir, exist_ok=True)

# Capture images from various angles with varying brightness and contrast
capture_images(output_dir, num_images_per_angle)