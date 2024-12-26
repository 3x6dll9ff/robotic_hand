# Robotic Hand Controlled via AI and Flask Server

## Project Description
This project is a robotic hand controlled using artificial intelligence and a wireless network. The control is achieved through hand movement tracking using MediaPipe and OpenCV. Motion data is transmitted to an Arduino via a Flask server, enabling seamless wireless communication.

## Key Features
- **Hand Movement Tracking:** Utilizes MediaPipe for detecting and tracking finger movements.
- **Angle Calculation:** Calculates finger movement angles for controlling the robotic hand's servos.
- **Servo Control:** Commands are sent wirelessly to the Arduino, which operates the servos.
- **Wireless Connectivity:** The system is entirely wireless, relying on a Flask server for communication.

## Technologies Used
- **MediaPipe and OpenCV:** For hand movement tracking.
- **Flask:** Web server for data transmission between the computer and Arduino.
- **Arduino:** For controlling the robotic hand's servos.

## Project Workflow
1. **Camera:** Captures hand movements.
2. **Flask Server:** Processes data and sends it to the Arduino.
3. **Arduino:** Operates the robotic hand's servos based on the received data.

## How to Run the Project
1. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Connect the Arduino to the network.
3. Start the Flask server:
   ```bash
   python server.py
   ```
4. Ensure the camera is set up and accurately tracking movements.
5. Control the robotic hand by performing gestures in front of the camera.

## Future Improvements
- Add feedback from servos for more precise control.
- Extend functionality for mobile device control.
- Integrate ESP32 to simplify wireless communication.

## Conclusion
This project showcases the potential of combining artificial intelligence and IoT to control robotic devices. It serves as a foundation for more advanced robotics systems.

