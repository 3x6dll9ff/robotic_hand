import threading
import cv2
import mediapipe as mp
import requests
import time
import math

time.sleep(2)

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)

valid_angles = [0, 30, 60, 90, 120, 150, 180]

prev_distances = [0, 0, 0, 0, 0]

# sensitivity 
sensitivity = {
    1: (30, 80),   # Thumb
    2: (20, 60),   # Index finger
    3: (20, 60),   # Middle finger
    4: (20, 60),   # Ring finger
    5: (20, 60),   # Pinky
}

#calculate angle 
def calculate_angle(distance, min_distance, max_distance):
    if distance < min_distance:
        distance = min_distance
    elif distance > max_distance:
        distance = max_distance

    angle = int(((distance - min_distance) / (max_distance - min_distance)) * 180)

    return min(max(angle, 0), 180)

# send data 
def send_to_arduino(pin, angle):
    url = "http://192.168.52.15:5000/send_to_arduino"
    data = f"PIN{pin}:ANGLE:{angle}\n"
    
    def send_request():
        try:
            response = requests.post(url, data=data)
            if response.status_code == 200:
                print(response.content)
            else:
                print(response.content)
        except requests.exceptions.RequestException as e:
            print(f"Error sending data to server: {e}")

    threading.Thread(target=send_request).start()


with mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            continue

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        # Display the result
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:

                finger_base_positions = [17, 13, 9, 5, 1]  
                finger_tip_positions = [20, 16, 12, 8, 4] 

                for i in range(5):  
                    if i == 4: 
                        point_a = hand_landmarks.landmark[4]  # Tip of thumb (ID 4)
                        point_b = hand_landmarks.landmark[5]  # Base of pinky (ID 5)
                    else:
                        point_a = hand_landmarks.landmark[finger_base_positions[i]]  # Base of the finger
                        point_b = hand_landmarks.landmark[finger_tip_positions[i]]  # Tip of the finger

                    # Get x, y coordinates for both points
                    x1, y1 = int(point_a.x * frame.shape[1]), int(point_a.y * frame.shape[0])
                    x2, y2 = int(point_b.x * frame.shape[1]), int(point_b.y * frame.shape[0])

                    cv2.putText(frame, f"{finger_base_positions[i]}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    cv2.putText(frame, f"{finger_tip_positions[i]}", (x2, y2 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

                    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

                    min_distance, max_distance = sensitivity[i + 1]

                    # If it's the thumb, send only 0 or 90
                    if i == 0: 
                        if distance < min_distance:  
                            send_to_arduino(i + 2, 0)
                        elif distance > max_distance:  
                            send_to_arduino(i + 2, 90)
                    else:  
                        angle = calculate_angle(distance, min_distance, max_distance)

                        if abs(distance - prev_distances[i]) > 2: 
                            send_to_arduino(i + 2, angle)

                            prev_distances[i] = distance

                    cv2.putText(frame, f"Dist {i + 1}: {int(distance)}", (50, 50 + i * 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                    cv2.circle(frame, (x1, y1), 5, (0, 255, 0), -1)  # Base point of the finger
                    cv2.circle(frame, (x2, y2), 5, (0, 0, 255), -1)  # Tip point of the finger

                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        cv2.imshow('Hand Tracking', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
