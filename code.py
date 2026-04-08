import cv2
import mediapipe as mp
import numpy as np
from collections import deque

# Initialize MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)
mp_drawing = mp.solutions.drawing_utils

# Initialize webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Get frame dimensions
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Create canvas for drawing
canvas = np.ones((frame_height, frame_width, 3), np.uint8) * 255

# Deque to store recent points for smooth drawing
points_queue = deque(maxlen=2)

# Color and drawing settings
drawing_color = (0, 0, 255)  # BGR format - Red
eraser_color = (255, 255, 255)  # White
brush_thickness = 5
eraser_thickness = 30

# State variables
is_drawing = False
is_erasing = False
hand_detected = False
gesture_timer = 0

def distance(p1, p2):
    """Calculate Euclidean distance between two points"""
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def get_hand_position(hand_landmarks, frame_width, frame_height):
    """Get index finger tip position from hand landmarks"""
    # Index finger tip is landmark 8
    index_tip = hand_landmarks.landmark[8]
    x = int(index_tip.x * frame_width)
    y = int(index_tip.y * frame_height)
    return (x, y)

def is_pointing_gesture(hand_landmarks):
    """Check if hand is in pointing gesture (index finger extended)"""
    # Index finger tip (8) should be above index finger PIP (6)
    # and middle finger should be curled
    index_tip = hand_landmarks.landmark[8]
    index_pip = hand_landmarks.landmark[6]
    middle_tip = hand_landmarks.landmark[12]
    middle_pip = hand_landmarks.landmark[10]
    
    # Index finger extended upward
    index_extended = index_tip.y < index_pip.y
    # Middle finger curled
    middle_curled = middle_tip.y > middle_pip.y
    
    return index_extended and middle_curled

def is_peace_gesture(hand_landmarks):
    """Check if hand is in peace gesture (for erasing)"""
    index_tip = hand_landmarks.landmark[8]
    index_pip = hand_landmarks.landmark[6]
    middle_tip = hand_landmarks.landmark[12]
    middle_pip = hand_landmarks.landmark[10]
    ring_tip = hand_landmarks.landmark[16]
    ring_pip = hand_landmarks.landmark[14]
    
    # Index and middle finger extended, ring and pinky curled
    index_extended = index_tip.y < index_pip.y
    middle_extended = middle_tip.y < middle_pip.y
    ring_curled = ring_tip.y > ring_pip.y
    
    return index_extended and middle_extended and ring_curled

def is_stop_gesture(hand_landmarks):
    """Check if hand is open (all fingers extended) - for clearing"""
    wrist = hand_landmarks.landmark[0]
    fingers_tips = [
        hand_landmarks.landmark[4],   # Thumb
        hand_landmarks.landmark[8],   # Index
        hand_landmarks.landmark[12],  # Middle
        hand_landmarks.landmark[16],  # Ring
        hand_landmarks.landmark[20]   # Pinky
    ]
    
    # All finger tips should be far from wrist
    all_extended = all(
        distance((tip.x, tip.y), (wrist.x, wrist.y)) > 0.3 
        for tip in fingers_tips
    )
    
    return all_extended

def draw_ui(frame, is_drawing, is_erasing, hand_detected):
    """Draw UI elements on the frame"""
    height, width = frame.shape[:2]
    
    # Draw mode indicator
    if is_drawing:
        cv2.putText(frame, "MODE: DRAWING", (20, 40), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    elif is_erasing:
        cv2.putText(frame, "MODE: ERASING", (20, 40), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)
    else:
        cv2.putText(frame, "MODE: IDLE", (20, 40), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (100, 100, 100), 2)
    
    # Hand detection status
    status_color = (0, 255, 0) if hand_detected else (0, 0, 255)
    cv2.putText(frame, f"Hand: {'DETECTED' if hand_detected else 'NOT DETECTED'}", 
               (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, status_color, 2)
    
    # Instructions
    instructions = [
        "GESTURES:",
        "ONE FINGER UP -> DRAW",
        "PEACE SIGN -> ERASE",
        "OPEN HAND -> CLEAR",
        "PRESS 'C' -> CLEAR",
        "PRESS 'ESC' -> EXIT"
    ]
    
    y_offset = height - 20 * len(instructions)
    for i, instruction in enumerate(instructions):
        cv2.putText(frame, instruction, (20, y_offset + i * 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)

def main():
    global canvas, points_queue, is_drawing, is_erasing, hand_detected, gesture_timer, drawing_color
    
    fps_clock = cv2.getTickCount()
    fps = 0
    
    print("=== AIR DRAWER ===")
    print("Gestures:")
    print("  1 Finger UP -> Draw")
    print("  Peace Sign (2 fingers UP) -> Erase")
    print("  Open Hand (all fingers) -> Clear")
    print("  'C' key -> Clear canvas")
    print("  'ESC' key -> Exit")
    print()
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Flip for selfie view
        frame = cv2.flip(frame, 1)
        h, w, c = frame.shape
        
        # Convert to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)
        
        hand_detected = results.multi_hand_landmarks is not None
        
        # Process hand landmarks
        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            index_pos = get_hand_position(hand_landmarks, w, h)
            
            # Determine gesture
            if is_stop_gesture(hand_landmarks):
                gesture_timer += 1
                if gesture_timer > 20:  # Hold for 20 frames to clear
                    canvas = np.ones((h, w, 3), np.uint8) * 255
                    points_queue.clear()
                    gesture_timer = 0
                    print("Canvas cleared!")
            else:
                gesture_timer = 0
            
            if is_peace_gesture(hand_landmarks):
                is_erasing = True
                is_drawing = False
                # Erase on canvas
                cv2.circle(canvas, index_pos, eraser_thickness, 
                          eraser_color, -1)
                cv2.circle(frame, index_pos, eraser_thickness, 
                          (0, 165, 255), 2)
            elif is_pointing_gesture(hand_landmarks):
                is_drawing = True
                is_erasing = False
                # Add to queue and draw
                points_queue.append(index_pos)
                
                if len(points_queue) == 2:
                    cv2.line(canvas, points_queue[0], points_queue[1],
                            drawing_color, brush_thickness)
                
                # Draw indicator
                cv2.circle(frame, index_pos, 8, drawing_color, -1)
            else:
                is_drawing = False
                is_erasing = False
                points_queue.clear()
            
            # Draw hand landmarks
            mp_drawing.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2)
            )
        else:
            is_drawing = False
            is_erasing = False
            points_queue.clear()
        
        # Blend canvas with camera feed
        alpha = 0.7
        blended = cv2.addWeighted(frame, alpha, canvas, 1 - alpha, 0)
        
        # Draw UI
        draw_ui(blended, is_drawing, is_erasing, hand_detected)
        
        # FPS calculation
        fps_new = cv2.getTickFrequency() / (cv2.getTickCount() - fps_clock)
        fps = 0.7 * fps + 0.3 * fps_new
        fps_clock = cv2.getTickCount()
        
        cv2.putText(blended, f"FPS: {fps:.1f}", (w - 150, 40),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Display
        cv2.imshow("Air Drawer", blended)
        
        # Handle key presses
        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # ESC
            break
        elif key == ord('c') or key == ord('C'):
            canvas = np.ones((h, w, 3), np.uint8) * 255
            points_queue.clear()
            print("Canvas cleared!")
        elif key == ord('r') or key == ord('R'):
            # Cycle through colors
            color_options = [(0, 0, 255), (0, 255, 0), (255, 0, 0), 
                            (0, 255, 255), (255, 0, 255), (255, 255, 0)]
            current_idx = color_options.index(drawing_color) if drawing_color in color_options else 0
            drawing_color = color_options[(current_idx + 1) % len(color_options)]
            print(f"Color changed to: {drawing_color}")
    
    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    hands.close()
    print("Air Drawer closed!")

if __name__ == "__main__":
    main()
