# Pupil Neon ROS 2

ROS 2 integration for streaming scene video, gaze, eye events, eye state, and
IMU data from [Pupil Labs Neon](https://pupil-labs.com/products/neon). The
package provides two publisher nodes:

- **Simple publisher** — a small, synchronous scene-camera and gaze bridge.
  Use it for quick prototypes, teaching, or applications that only need an
  image, a 2D gaze point, and camera calibration.
- **Asynchronous publisher** — concurrent streams for scene video, detailed
  gaze/eye data, gaze events, IMU, and calibration. Use it for experiments,
  multimodal recording, or applications that must avoid one sensor stream
  blocking the others.

Both nodes use the
[Pupil Labs Realtime API](https://pupil-labs-realtime-api.readthedocs.io/en/stable/) and require the computer and Neon Companion device to be on the same network.
The asynchronous node discovers Neon automatically. 
The simple node uses the IP address and port in `config/params.yaml` (defaults: `10.0.0.2` and `8080`).

## Supported environment

This branch targets Ubuntu 22.04 and ROS 2 Humble. A working ROS 2 installation
and configured `rosdep` are assumed below.

## Dependencies

Install the build tools and ROS dependencies:

```bash
sudo apt update
sudo apt install -y \
  python3-colcon-common-extensions \
  python3-pip \
  python3-rosdep \
  ros-humble-cv-bridge \
  ros-humble-rqt-image-view \
  ros-humble-rviz2 \
  ros-humble-tf2-ros
```

Install the Pupil Labs API and Python image-processing dependencies. It depends on ```numpy``` and ```opencv-python```, which are likely already installed by ROS or the system package manager:

```bash
python3 -m pip install --user pupil-labs-realtime-api
```

And source from the root of your ROS 2 workspace:

```bash
source /opt/ros/humble/setup.bash
```

## Build

Clone this repository into the workspace's `src` directory, then build and
source the overlay:

```bash
cd ~/ros2_ws
colcon build --symlink-install --packages-select pupil_neon_ros
source install/setup.bash
```

Repeat the last command in every new terminal, after sourcing
`/opt/ros/humble/setup.bash`.

## Connect the glasses

1. Start the Neon Companion app and connect the glasses to the Companion device. When the glasses appear on the app, you can get a preview. 
2. Put the ROS computer and Companion device on the same network (wired or Wi-Fi, wired recommended). A phone hotspot shared by both devices also works, but the **wired adapter offers much better results**. You can check the IP address by tapping on the top right, 
3. Keep the Companion app open, then start one publisher below.

## Simple publisher

The simple publisher performs blocking reads for one scene frame and one gaze
sample on each ROS timer callback. It is easy to understand and has a small
topic surface, but a delayed sensor read can delay the other publications.

Launch it with the settings in `config/params.yaml`:

```bash
ros2 launch pupil_neon_ros pupil.launch.py
```

Or run it directly and override connection settings:

```bash
ros2 run pupil_neon_ros pupil_publisher.py --ros-args \
  -p ip:="10.0.0.2" \
  -p port:="8080" \
  -p publish_freq:=30
```

| Topic | Type | Description |
| --- | --- | --- |
| `/pupil_glasses/front_camera/image_color` | `sensor_msgs/msg/Image` | Uncompressed BGR scene image |
| `/pupil_glasses/front_camera/camera_info` | `sensor_msgs/msg/CameraInfo` | Scene-camera calibration |
| `/pupil_glasses/gaze_position` | `geometry_msgs/msg/PointStamped` | Normalized image coordinates (`x` and `y` are approximately 0–1); `z` is `camera_depth` |

Simple-node parameters are defined under `/pupil_glasses_node` in
`config/params.yaml`: `ip`, `port`, `publish_freq`, `video_resolution`,
`camera_depth`, `draw_circle`, and `print_performance`. 

## Asynchronous publisher

The asynchronous publisher discovers a Neon device, starts independent video, gaze, eye-event, and IMU streams in an asyncio loop, and publishes them from a background thread. 
Its launch file also starts an RViz marker publisher (it does not open RViz itself).

```bash
ros2 launch pupil_neon_ros async_pupil.launch.py
```

To run only the publisher, or reduce image bandwidth to 50% in each dimension:

```bash
ros2 run pupil_neon_ros async_pupil_publisher.py --ros-args \
  -p image_scale:=0.5
```

`image_scale` defaults to `1.0`. It scales the compressed scene image, gaze
pixel coordinates, event pixel measurements, and camera intrinsics together.

| Topic | Type | Description |
| --- | --- | --- |
| `/pupil_glasses/front_image` | `sensor_msgs/msg/CompressedImage` | JPEG-compressed scene image |
| `/pupil_glasses/front_camera/camera_info` | `sensor_msgs/msg/CameraInfo` | Scaled fisheye camera calibration |
| `/pupil_glasses/gaze_position` | `geometry_msgs/msg/PointStamped` | Gaze position in scaled image pixels |
| `/pupil_glasses/gaze_data` | `pupil_neon_ros/msg/GazeData` | Gaze plus per-eye pupil, eyeball, optical-axis, and eyelid fields |
| `/pupil_glasses/event/saccade` | `pupil_neon_ros/msg/GazeEvent` | Completed saccades |
| `/pupil_glasses/event/fixation` | `pupil_neon_ros/msg/GazeEvent` | Completed fixations |
| `/pupil_glasses/event/saccade_onset` | `pupil_neon_ros/msg/GazeEvent` | Saccade onset events |
| `/pupil_glasses/event/fixation_onset` | `pupil_neon_ros/msg/GazeEvent` | Fixation onset events |
| `/pupil_glasses/event/blink` | `pupil_neon_ros/msg/GazeEvent` | Blink events |
| `/pupil_glasses/imu` | `sensor_msgs/msg/Imu` | Orientation, angular velocity, and linear acceleration |
| `/tf_static` | `tf2_msgs/msg/TFMessage` | Static `world` to `camera_optical_frame` transform |

The launch file's visualizer additionally publishes `/visuals/gaze_point_marker`, `/visuals/gaze_vector_marker`, and `/visuals/eye_markers`. 
Open RViz separately with `rviz2` and add Marker and MarkerArray displays if those visualizations are useful.

### Local CSV logging

Starting the asynchronous node creates `user_recordings/session_<YYYYMMDD_HHMMSS>/` below the process's current working directory. 
It continuously writes:

- `pupilometry.csv` — pupil diameters and gaze position
- `saccade_events.csv` — completed saccades and fixations
- `imu_data.csv` — accelerometer, gyroscope, and magnitude values

This logging is always enabled in the current implementation. 
Ensure the working directory is writable and has sufficient disk space.

## Useful commands

Inspect live topics and rates:

```bash
ros2 topic list
ros2 topic hz /pupil_glasses/front_image
ros2 topic echo /pupil_glasses/gaze_position
ros2 topic echo /pupil_glasses/imu
```

View the simple node's raw image or the asynchronous node's compressed image:

```bash
ros2 run rqt_image_view rqt_image_view \
  /pupil_glasses/front_camera/image_color

ros2 run rqt_image_view rqt_image_view /pupil_glasses/front_image
```

Record all principal asynchronous-node topics and replay them with a simulated
clock:

```bash
ros2 bag record -o neon_recording /pupil_glasses/front_image \
  /pupil_glasses/front_camera/camera_info \
  /pupil_glasses/gaze_position /pupil_glasses/gaze_data \
  /pupil_glasses/imu /pupil_glasses/event/saccade \
  /pupil_glasses/event/fixation /pupil_glasses/event/blink

ros2 bag play neon_recording --clock --loop
```

## Troubleshooting

- **No device could be found:** confirm both devices are on the same subnet,  disable client isolation, and allow multicast through the firewall.
- **No sensor data:** ensure the Companion app is running and the glasses are connected. Try to disconnect and connect the cable again. 
- **Simple node cannot connect:** update `ip` and `port` in `config/params.yaml`, or use the direct-run overrides above.
- **No eye events or IMU:** the asynchronous node requires gaze, scene, eye-event, and IMU sensors to report as connected before streaming.
- **High CPU/network use:** run the asynchronous node with a smaller  `image_scale`, such as `0.5`.

## Docker

A `Dockerfile` is included for development. Hardware access, host networking,
and GUI forwarding are platform-specific; for first-time setup, the native ROS
2 workflow above is the simplest supported path.

## License

GNU General Public License v3.0. See `LICENSE`.
