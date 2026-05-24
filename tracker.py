import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Pose and Drawing utilities
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def calculate_angle(a, b, c):
    """
    Calculates the angle between three coordinates.
    A = First point (e.g., Shoulder)
    B = Mid point / Vertex (e.g., Elbow)
    C = End point (e.g., Wrist)
    """
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End
    
    # Calculate the angle using arctangent (from your mathematical logic)
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    
    # Ensure the angle doesn't exceed 180 degrees for standard joint mechanics
    if angle > 180.0:
        angle = 360 - angle
        
    return angle

def main():
    # Start Video Capture (0 is usually the built-in webcam)
    cap = cv2.VideoCapture(0)
    
    # Repetition Counter & State Machine Variables
    counter = 0 
    stage = None # Will hold 'up' or 'down'

    # Setup MediaPipe instance
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            # Recolor image to RGB (MediaPipe requires RGB, OpenCV uses BGR)
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            
            # Make detection
            results = pose.process(image)
            
            # Recolor back to BGR for OpenCV rendering
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark
                
                # Get coordinates for the Left Arm (Shoulder, Elbow, Wrist)
                # You can change these to track legs (Hip, Knee, Ankle) for squats!
                shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                
                # Calculate dynamic angle
                angle = calculate_angle(shoulder, elbow, wrist)
                
                # Visualize the angle at the elbow vertex
                # Multiply by 640, 480 (standard webcam resolution) to map normalized coordinates to pixels
                cv2.putText(image, str(int(angle)), 
                           tuple(np.multiply(elbow, [640, 480]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                
                # Form State Machine logic (Bicep Curl thresholds)
                if angle > 160:
                    stage = "down"
                if angle < 30 and stage == 'down':
                    stage = "up"
                    counter += 1
                    print(f"Rep Count: {counter}")
                       
            except Exception as e:
                # Passes if landmarks aren't visible in the frame
                pass
            
            # Render a UI Box for the rep counter
            cv2.rectangle(image, (0,0), (250,73), (245,117,16), -1)
            
            # Display Rep Data
            cv2.putText(image, 'REPS', (15,12), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, str(counter), 
                        (10,60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
            
            # Display Stage Data
            cv2.putText(image, 'STAGE', (95,12), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, stage, 
                        (90,60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
            
            # Render skeletal connections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                    mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                     )               
            
            # Show the final image
            cv2.imshow('AI Biomechanics Tracker', image)

            # Break the loop if the 'q' key is pressed
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

    # Clean up
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
