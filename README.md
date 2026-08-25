# pupil_neon_ros (release 2.0 docs)

ROS 2 integration for Pupil Neon glasses.

This project publishes:
- `pupil_glasses/front_camera/image_color` (`sensor_msgs/Image`)
- `pupil_glasses/front_camera/camera_info` (`sensor_msgs/CameraInfo`)
- `pupil_glasses/gaze_position` (`geometry_msgs/PointStamped`)

## Branches and node variants

- `release` / `copilot/release-20-update-documentation` (this branch): simple publisher flow (`pupil_publisher.py`) plus emulator.
- `humble` and `recording_button`: include the asynchronous publisher flow (`async_pupil_publisher.py`) and RViz helper.

If you need async streaming specifically, use `humble` or `recording_button`.

## Prerequisites

- ROS 2 Humble workspace
- Pupil Labs Realtime API Python package
- Glasses and ROS machine on the same network

## Build

```bash
colcon build
source install/setup.bash
```

## Run (simple node, this branch)

```bash
ros2 launch pupil_neon_pkg pupil.launch.py
```

## Run emulator (this branch)

```bash
ros2 launch pupil_neon_pkg emulator_pupil.launch.py
```

## Run async node (humble / recording_button)

```bash
ros2 launch pupil_neon_ros async_pupil.launch.py
```

## Configuration

Runtime parameters are in:

`config/params.yaml`

Common parameters:
- `publish_freq`
- `video_resolution`
- `ip`
- `port`
- `draw_circle`
- `print_performance`

## Docker (optional)

```bash
xhost +local:root
docker image build -t ros2-glass-base .
docker run -it --env="DISPLAY" --device=/dev/video0:/dev/video0 -e DISPLAY=$DISPLAY --env="QT_X11_NO_MITSHM=1" --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" --privileged --net=host -v /dev/shm:/dev/shm ros2-glass-base
```
