import time
import head_pose

# Global variables
GLOBAL_CHEAT = 0
PERCENTAGE_CHEAT = 0
CHEAT_THRESHOLD = 0.6

def simple_cheat_detection():
    """Simple cheat detection based on head pose flags"""
    global GLOBAL_CHEAT, PERCENTAGE_CHEAT
    
    # Basic logic: if either axis shows cheating, increase probability
    if head_pose.X_AXIS_CHEAT == 1 or head_pose.Y_AXIS_CHEAT == 1:
        PERCENTAGE_CHEAT = min(1.0, PERCENTAGE_CHEAT + 0.1)
    else:
        PERCENTAGE_CHEAT = max(0.0, PERCENTAGE_CHEAT - 0.05)
    
    # Set global cheat flag if above threshold
    if PERCENTAGE_CHEAT > CHEAT_THRESHOLD:
        GLOBAL_CHEAT = 1
    else:
        GLOBAL_CHEAT = 0
    
    print(f"Cheat Probability: {PERCENTAGE_CHEAT:.2f}, Cheating: {GLOBAL_CHEAT}")

def run_simple_detection():
    """Run simplified detection without graphs"""
    while True:
        simple_cheat_detection()
        time.sleep(1)  # Check once per second

# Backward compatibility - original function names
def process():
    simple_cheat_detection()

def run_detection():
    run_simple_detection()

# Ultra-simple version for basic face detection
def basic_face_monitoring():
    """Even simpler version - just use head_pose flags directly"""
    global GLOBAL_CHEAT
    
    # Direct mapping: if head_pose says cheating, then we say cheating
    if head_pose.X_AXIS_CHEAT == 1 or head_pose.Y_AXIS_CHEAT == 1:
        GLOBAL_CHEAT = 1
    else:
        GLOBAL_CHEAT = 0
    
    return GLOBAL_CHEAT

# For even simpler integration
def get_cheat_status():
    """One-line function to get current cheat status"""
    return basic_face_monitoring()

def get_cheat_probability():
    """Get simple probability (0 or 1)"""
    return 1.0 if basic_face_monitoring() else 0.0