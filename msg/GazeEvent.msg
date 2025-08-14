# FixationEvent.msg
# Full fixation or saccade event data
# event_type: 0 for saccades, 1 for fixations

std_msgs/Header header
uint8 event_type
uint64 start_time_ns
uint64 end_time_ns
float32 start_gaze_x
float32 start_gaze_y
float32 end_gaze_x
float32 end_gaze_y
float32 mean_gaze_x
float32 mean_gaze_y
float32 amplitude_pixels
float32 amplitude_angle_deg
float32 mean_velocity
float32 max_velocity
float64 rtp_ts_unix_seconds
