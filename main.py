import cv2
import mediapipe as mp
import serial
import time

# Initialize serial communication with Arduino
arduino = serial.Serial('COM4', 9600, timeout=1)  # Adjust 'COM3' to your Arduino's port
time.sleep(2)

# Initialize Mediapipe for hand tracking
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

# Initialize camera
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame horizontally for a later selfie-view display
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    # Convert the BGR image to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the image and detect hands
    result = hands.process(rgb_frame)

    # Draw hand landmarks
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Count fingers
            finger_count = 0

            # Get landmarks of each finger tip
            landmarks = hand_landmarks.landmark
            if landmarks[mp_hands.HandLandmark.THUMB_TIP].x > landmarks[mp_hands.HandLandmark.THUMB_IP].x:
                finger_count += 1
            if landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP].y < landmarks[mp_hands.HandLandmark.INDEX_FINGER_PIP].y:
                finger_count += 1
            if landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y < landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y:
                finger_count += 1
            if landmarks[mp_hands.HandLandmark.RING_FINGER_TIP].y < landmarks[mp_hands.HandLandmark.RING_FINGER_PIP].y:
                finger_count += 1
            if landmarks[mp_hands.HandLandmark.PINKY_TIP].y < landmarks[mp_hands.HandLandmark.PINKY_PIP].y:
                finger_count += 1

            # Send the number of fingers to Arduino
            arduino.write(str(finger_count).encode())

    # Display the resulting frame
    cv2.imshow('Finger Counting', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up
cap.release()
cv2.destroyAllWindows()
arduino.close()
