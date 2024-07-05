import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    launch_description = LaunchDescription()

    config = os.path.join(
        get_package_share_directory("pupil_neon_pkg"), "config", "params.yaml"
    )

    pupil_node = Node(
        package="pupil_neon_pkg",
        executable="emulator_publisher.py",
        name="glasses_emulator_node",
        arguments=[("__log_level:=debug")],
        output="screen",
        parameters=[config],
    )
    launch_description.add_action(pupil_node)

    print("Pupil Neon Emulator Launch is Running...")
    print(f"params.yaml: {config}")

    return launch_description
