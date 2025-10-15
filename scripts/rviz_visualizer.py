#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Point
from visualization_msgs.msg import Marker, MarkerArray
from pupil_neon_ros.msg import GazeData  # Your custom msg


class PupilRvizVisualizer(Node):
    def __init__(self):
        super().__init__("pupil_rviz_visualizer")

        # Publishers
        self.gaze_point_pub = self.create_publisher(
            Marker, "visuals/gaze_point_marker", 50
        )
        self.gaze_vector_pub = self.create_publisher(
            Marker, "visuals/gaze_vector_marker", 50
        )
        # Switch to MarkerArray for eyes
        self.eye_pub = self.create_publisher(MarkerArray, "visuals/eye_markers", 50)

        # Subscribe to GazeData
        self.create_subscription(
            GazeData, "pupil_glasses/gaze_data", self.gaze_callback, 100
        )

        self.counter = 0
        self.get_logger().info("Pupil RViz Visualizer Node started")

    def gaze_callback(self, msg: GazeData):
        self.get_logger().debug(f"Received gaze data: {msg}")
        self.counter += 1
        if self.counter % 20 != 0:  # throttle publishing
            return

        # ---- Gaze point and vector ----
        self.publish_gaze_point(msg)
        self.publish_gaze_vector(msg)

        # ---- Eyes and eye axes ----
        marker_array = MarkerArray()

        # Eyes
        marker_array.markers.append(
            self.make_eye_marker(
                msg.left_eye, msg.header, eye_id=0, color=(0.0, 0.0, 1.0)
            )
        )
        marker_array.markers.append(
            self.make_eye_marker(
                msg.right_eye, msg.header, eye_id=1, color=(1.0, 0.0, 0.0)
            )
        )

        # Eye axes
        marker_array.markers.append(
            self.make_axis_marker(
                msg.left_eye, msg.header, eye_id=2, color=(0.0, 1.0, 1.0)
            )
        )
        marker_array.markers.append(
            self.make_axis_marker(
                msg.right_eye, msg.header, eye_id=3, color=(1.0, 0.0, 1.0)
            )
        )

        self.eye_pub.publish(marker_array)

    # ---------------- OLD FUNCTIONS ----------------
    def publish_gaze_point(self, gaze_msg: GazeData, scale=0.02):
        marker = Marker()
        marker.header = gaze_msg.header
        marker.ns = "gaze_point"
        marker.id = 10
        marker.type = Marker.SPHERE
        marker.action = Marker.ADD
        marker.pose.position.x = gaze_msg.x
        marker.pose.position.y = gaze_msg.y
        marker.pose.position.z = 0.0
        marker.pose.orientation.w = 1.0
        marker.scale.x = marker.scale.y = marker.scale.z = scale
        marker.color.r = 1.0
        marker.color.g = 0.0
        marker.color.b = 0.0
        marker.color.a = 1.0
        self.gaze_point_pub.publish(marker)

    def publish_gaze_vector(self, gaze_msg: GazeData, scale=0.1):
        marker = Marker()
        marker.header = gaze_msg.header
        marker.ns = "gaze_vector"
        marker.id = 11
        marker.type = Marker.ARROW
        marker.action = Marker.ADD

        start = Point(x=0.0, y=0.0, z=0.0)
        end = Point(
            x=gaze_msg.x * scale,
            y=gaze_msg.y * scale,
            z=0.0,
        )
        marker.points = [start, end]

        marker.scale.x = 0.005
        marker.scale.y = 0.01
        marker.scale.z = 0.02

        marker.color.r = 0.0
        marker.color.g = 1.0
        marker.color.b = 0.0
        marker.color.a = 1.0

        self.gaze_vector_pub.publish(marker)

    # ---------------- NEW FUNCTIONS (MarkerArray-friendly) ----------------
    def make_eye_marker(self, eye, header, eye_id, color, scale=0.0242):
        marker = Marker()
        marker.header = header
        marker.ns = "eyes"
        marker.id = eye_id
        marker.type = Marker.SPHERE
        marker.action = Marker.ADD
        marker.pose.position.x = eye.eyeball_center_x / 1000
        marker.pose.position.y = eye.eyeball_center_y / 1000
        marker.pose.position.z = eye.eyeball_center_z / 1000
        marker.pose.orientation.w = 1.0
        marker.scale.x = marker.scale.y = marker.scale.z = scale
        marker.color.r, marker.color.g, marker.color.b = color
        marker.color.a = 1.0
        return marker

    def make_axis_marker(self, eye, header, eye_id, color, scale=1.0):
        marker = Marker()
        marker.header = header
        marker.ns = "eye_axes"
        marker.id = eye_id
        marker.type = Marker.ARROW
        marker.action = Marker.ADD

        start = Point(
            x=eye.eyeball_center_x / 1000,
            y=eye.eyeball_center_y / 1000,
            z=eye.eyeball_center_z / 1000,
        )
        end = Point(
            x=(eye.eyeball_center_x / 1000 + eye.optical_axis_x) * scale,
            y=(eye.eyeball_center_y / 1000 + eye.optical_axis_y) * scale,
            z=(eye.eyeball_center_z / 1000 + eye.optical_axis_z) * scale,
        )
        marker.points = [start, end]

        marker.scale.x = 0.01
        marker.scale.y = 0.01
        marker.scale.z = 0.0

        marker.color.r, marker.color.g, marker.color.b = color
        marker.color.a = 1.0
        return marker


def main(args=None):
    rclpy.init(args=args)
    node = PupilRvizVisualizer()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
