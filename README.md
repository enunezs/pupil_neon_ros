# ros2_pupil_neon

Simple Pupil Neon interfacing for ROS2.

Provides and publishes messages with the [Pupil Neon Glasses](https://pupil-labs.com/products/neon) basic API elements: `pupil_glasses/front_camera` and `pupil_glasses/gaze_position`.

The script has customizable variables to configure resolution, frequency and other variables, as well as using a webcam for emulation

Using the Pupil Labs Realtime API [pupil-labs-realtime-api
](https://pupil-labs-realtime-api.readthedocs.io/en/stable/api/index.html).

# Usage

To use, clone the repository to your workspace, connect on the same wifi network as the Pupil Glasses (or share connection on the phone and connect) and run:

```
colcon build
source install/setup
ros2 launch pupil_neon_pkg pupil.launch.py
```

A node to emulate glasses behaviour using a webcame and mouse (useful for development!) can be instantiated with:

```
colcon build
source install/setup
ros2 launch pupil_neon_pkg pupil_devel.launch.py
```



Alternatively, run the associated as a docker container with the provided Dockerfile

```
xhost +local:root

docker image build -t ros2-glass-base .

docker run -it --env="DISPLAY" --device=/dev/video0:/dev/video0 -e DISPLAY=$DISPLAY --env="QT_X11_NO_MITSHM=1" --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" --privileged --net=host -v /home/ema/Documents/ROS2_Workspaces/:/home/username/workspaces -v /dev/shm:/dev/shm ros2-glass-base

export containerId=$(docker ps -l -q)

```

Multiple parameters can be configured at: ```config/params.yaml```


<!--
# Citation

'''
@inproceedings{Nunez:2022,
Pennding
}
'''
-->
