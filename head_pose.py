import cv2
import numpy as np

# Global variables
x = 0
y = 0
X_AXIS_CHEAT = 0
Y_AXIS_CHEAT = 0

def pose():
    global x, y, X_AXIS_CHEAT, Y_AXIS_CHEAT
    
    # Load face detection classifier
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            continue
            
        # Convert to grayscale for face detection
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        # Reset cheat flags
        X_AXIS_CHEAT = 0
        Y_AXIS_CHEAT = 0
        
        if len(faces) > 0:
            # Get the first face detected
            (x, y, w, h) = faces[0]
            
            # Simple head position estimation based on face position
            img_h, img_w = image.shape[:2]
            center_x = x + w/2
            center_y = y + h/2
            
            # Calculate normalized position (0-1, where 0.5 is center)
            norm_x = center_x / img_w
            norm_y = center_y / img_h
            
            # Simple cheat detection based on face position
            # If face is too far from center, mark as suspicious
            if abs(norm_x - 0.5) > 0.3:  # Too far left or right
                X_AXIS_CHEAT = 1
            else:
                X_AXIS_CHEAT = 0
                
            if abs(norm_y - 0.5) > 0.3:  # Too far up or down
                Y_AXIS_CHEAT = 1
            else:
                Y_AXIS_CHEAT = 0
                
            # Draw rectangle around face for visualization (optional)
            cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)
            
            # Display status
            status = "FACE DETECTED"
            if X_AXIS_CHEAT or Y_AXIS_CHEAT:
                status = "SUSPICIOUS MOVEMENT"
                cv2.putText(image, status, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            else:
                cv2.putText(image, status, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        else:
            # No face detected - mark as cheating
            X_AXIS_CHEAT = 1
            Y_AXIS_CHEAT = 1
            cv2.putText(image, "NO FACE DETECTED", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # Optional: Display the camera feed (comment out to run in background)
        # cv2.imshow('Face Detection', image)
        
        # Break on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Simple version without display window
def pose_simple():
    global X_AXIS_CHEAT, Y_AXIS_CHEAT
    
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            continue
            
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        # Simple logic: if no face or face position is suspicious
        if len(faces) == 0:
            X_AXIS_CHEAT = 1
            Y_AXIS_CHEAT = 1
        else:
            # Basic position check
            (x, y, w, h) = faces[0]
            img_h, img_w = image.shape[:2]
            center_x = x + w/2
            center_y = y + h/2
            
            # Mark as suspicious if face is not in center area
            if abs(center_x/img_w - 0.5) > 0.3 or abs(center_y/img_h - 0.5) > 0.3:
                X_AXIS_CHEAT = 1
                Y_AXIS_CHEAT = 1
            else:
                X_AXIS_CHEAT = 0
                Y_AXIS_CHEAT = 0

    cap.release()