from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess


def generate_launch_description():
    return LaunchDescription([
        Node(
            package="pupil_neon_pkg",
            executable="pupil_publisher.py",
            name="pupil_node",
            #prefix=['Terminal -e gdb -ex run --args'],
            arguments=[('__log_level:=debug')],
            output='screen'
        )
    ])
