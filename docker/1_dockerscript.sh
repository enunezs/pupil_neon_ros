xhost +local:root

docker image build -t ros2_pupil_neon .     

docker run -it --env="DISPLAY" \
	--device=/dev/video0:/dev/video0 \
	-e DISPLAY=$DISPLAY \
	--env="QT_X11_NO_MITSHM=1" \
	--volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
	--privileged \
	-e "ROS_DOMAIN_ID=7" \
	--net=host \
	-v $(pwd):/root/ws/ros2_pupil_neon \
	-v /dev/shm:/dev/shm \
	ros2_pupil_neon

export containerId=$(docker ps -l -q)

