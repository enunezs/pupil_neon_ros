# msg/GazeData.msg
# Complete gaze data using modular Eye messages

std_msgs/Header header
float32 x                     # Gaze point x coordinate
float32 y                     # Gaze point y coordinate  
bool worn                     # Whether glasses are being worn
Eye left_eye                  # Left eye data
Eye right_eye                 # Right eye data
bool has_eye_state           # True if eye state data is available
bool has_eyelid_data         # True if eyelid data is available
float64 timestamp_unix_seconds
