# msg/Eye.msg
# Individual eye data for left or right eye

float32 pupil_diameter        # Pupil diameter in mm
float32 eyeball_center_x      # 3D eyeball center coordinates
float32 eyeball_center_y
float32 eyeball_center_z
float32 optical_axis_x        # 3D optical axis vector (normalized)
float32 optical_axis_y
float32 optical_axis_z
float32 eyelid_angle_top      # Eyelid angles (NaN if not available)
float32 eyelid_angle_bottom
float32 eyelid_aperture       # Eyelid aperture (NaN if not available)