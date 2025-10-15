import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    launch_description = LaunchDescription()

    config = os.path.join(
        get_package_share_directory("pupil_neon_ros"), "config", "params.yaml"
    )

    pupil_node = Node(
        package="pupil_neon_ros",
        executable="async_pupil_publisher.py",
        name="pupil_glasses_node",
        arguments=["__log_level:=debug"],
        output="screen",
        parameters=[config],
    )
    launch_description.add_action(pupil_node)

    pupil_visuals_node = Node(
        package="pupil_neon_ros",
        executable="rviz_visualizer.py",
        name="pupil_glasses_visuals_node",
        arguments=["__log_level:=debug"],
        output="screen",
        parameters=[config],
    )
    launch_description.add_action(pupil_visuals_node)

    print("Pupil Neon Launch is Running...")
    print(f"params.yaml: {config}")

    return launch_description
