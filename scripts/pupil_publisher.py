#! /usr/bin/env python3

# GNU V3.0
# Copyright: Emanuel Nunez Sardinha

# To run:
"""
ros2 run pupil_neon_pkg pupil_publisher.py --ros-args --params-file src/pupil_neon_pkg/config/params.yaml
"""

# TODO
# Benchmark -> test max refresh rate
# change to wired connection (buy adaptor)

# * Core ROS dependencies
import rclpy
from rclpy.node import Node

# * Image messaging and conversion
from cv_bridge import CvBridge

# * Core time dependencies
from datetime import datetime

# * Image messaging and conversion
from cv_bridge import CvBridge
from cv2 import cvtColor, COLOR_BGR2RGB, destroyAllWindows
from cv2 import circle as cv2_circle

# * Base messages
from sensor_msgs.msg import Image
from sensor_msgs.msg import CameraInfo
from geometry_msgs.msg import PointStamped

# * Pupil
from pupil_labs.realtime_api.simple import discover_one_device
from pupil_labs.realtime_api.simple import Device

### Settings ###
# Moved to config file
import csv


class pupilPublisher(Node):
    def __init__(self):
        super().__init__("pupil_glasses_node")
        self.get_logger().info("Pupil Neon Glasses Node is Running...")

        # * Intialize publishers
        self.publisher_front_camera = self.create_publisher(
            Image, "pupil_glasses/front_camera", 1
        )
        self.publisher_gaze_position = self.create_publisher(
            PointStamped, "pupil_glasses/gaze_position", 1
        )
        self.publisher_camera_info = self.create_publisher(
            CameraInfo, "pupil_glasses/front_camera/camera_info", 1
        )
        # self.publisher_internal_camera = self.create_publisher(Image, "pupil_glasses/internal_camera", 1 )

        # Declare and retrieve parameters
        self.publish_freq = self.declare_and_get_parameter("publish_freq", 30)
        self.draw_circle = self.declare_and_get_parameter("draw_circle", False)
        self.camera_depth = self.declare_and_get_parameter("camera_depth", 1.0)
        self.video_resolution = self.declare_and_get_parameter(
            "video_resolution", (1600, 1200)
        )
        self.glasses_ip = self.declare_and_get_parameter("ip", "192.168.1.118")
        self.glasses_port = self.declare_and_get_parameter("port", "8080")
        self.print_performance = self.declare_and_get_parameter(
            "print_performance", False
        )
        self.log_to_csv = self.declare_and_get_parameter("log_to_csv", False)
        self.recording = self.declare_and_get_parameter("recording", False)

        # Connect to glasses
        self.get_logger().info("Connecting to Pupil Glasses...")
        self.get_logger().info(f"IP: {self.glasses_ip}")
        self.get_logger().info(f"Port: {self.glasses_port}")
        self.connect_to_glasses(ip=self.glasses_ip, port=self.glasses_port)

        self.timer = self.create_timer(1.0 / self.publish_freq, self.publish_pupil_data)

        # If logging to CSV
        if self.log_to_csv:
            self.get_logger().info("Logging to CSV...")
            self.csv_file = open(
                f"pupil_glasses_data_{self.publish_freq}Hz.csv", mode="w"
            )
            self.csv_writer = csv.writer(
                self.csv_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
            )
            self.csv_writer.writerow(
                [
                    "ts",
                    "gaze_x",
                    "gaze_y",
                    "gaze_worn",
                    "frame_duration",
                    "gaze_duration",
                    "pack_duration",
                    "publish_duration",
                ]
            )

    def __del__(self):
        self.get_logger().info("Pupil Neon Glasses Node is Shutting Down...")
        if self.log_to_csv:
            self.csv_file.close()

        self.device.close()

    def declare_and_get_parameter(self, name, default):
        self.declare_parameter(name, default)
        self.get_logger().info(
            f"Loaded parameter {name}: {self.get_parameter(name).value}"
        )
        return self.get_parameter(name).value

    def connect_to_glasses(self, ip="192.168.1.108", port="8080"):

        device = Device(address=ip, port=port)
        self.get_logger().info(f"Phone IP address: {device.phone_ip}")
        self.get_logger().info(f"Phone name: {device.phone_name}")
        self.get_logger().info(f"Battery level: {device.battery_level_percent}%")
        self.get_logger().info(
            f"Free storage: {device.memory_num_free_bytes / 1024**3:.1f} GB"
        )
        self.get_logger().info(
            f"Serial number of connected glasses: {device.module_serial}"
        )

        calibration = device.get_calibration()
        self.get_logger().info(f"Camera Calibration Matrix: \n {calibration[0][2]}")
        self.get_logger().info(
            f"Camera Distortion Coefficients: \n {calibration[0][3]}"
        )

        self.device = device

        self.recording = False
        if self.recording:
            recording_id = device.recording_start()
            self.get_logger().info(f"Started recording with id {recording_id}")

        self.bridge = CvBridge()

    def publish_pupil_data(self):
        device = self.device
        start_timestamp = self.get_clock().now()

        ### * Get the frame
        # matched_video_and_gaze = device.receive_matched_scene_video_frame_and_gaze()
        front_camera_frame = device.receive_scene_video_frame()
        # front_camera_frame = matched_video_and_gaze.frame.bgr_pixels
        # gaze = matched_video_and_gaze.gaze

        frame_duration = (start_timestamp - self.get_clock().now()).nanoseconds

        ### * Get the gaze coordinates
        gaze = device.receive_gaze_datum()
        gaze_duration = (frame_duration - self.get_clock().now()).nanoseconds

        ### * Pack image into message
        if self.draw_circle and gaze.worn:  # and pupil_glasses_msg.status == 0:
            front_camera_frame = self.draw_circle(front_camera_frame, (gaze.x, gaze.y))
        img_msg = self.bridge.cv2_to_imgmsg(front_camera_frame.bgr_pixels, "bgr8")
        img_msg.header.stamp = self.get_clock().now().to_msg()
        img_msg.header.frame_id = "pupil_glasses_frame"

        ### * Pack gaze position into message
        gaze_msg = PointStamped()
        gaze_msg.point.x = gaze.x / 1600
        gaze_msg.point.y = gaze.y / 1200
        gaze_msg.point.z = self.camera_depth
        gaze_msg.header.stamp = self.get_clock().now().to_msg()
        gaze_msg.header.frame_id = "pupil_glasses_frame"

        pack_duration = (gaze_duration - self.get_clock().now()).nanoseconds

        ### * Publish the message
        self.publisher_front_camera.publish(img_msg)
        self.publisher_gaze_position.publish(gaze_msg)
        publish_duration = (pack_duration - self.get_clock().now()).nanoseconds

        ### * Log to csv
        if self.log_to_csv:
            self.csv_writer.writerow(
                [
                    start_timestamp,
                    gaze.x,
                    gaze.y,
                    gaze.worn,
                    frame_duration,
                    gaze_duration,
                    pack_duration,
                    publish_duration,
                ]
            )
        ### !  Print performance
        """if self.print_performance:
            self.get_logger().info(
                f"Frame received at {dt.hour}:{dt.minute}:{dt.second}.{dt.microsecond} -> Published at {start_time.hour}:{start_time.minute}:{start_time.second}.{start_time.nanosecond}"
            )"""

    # Draw circle on image given gaze position
    def draw_circle(self, image, gaze_position):
        image_size = image.shape[:2][::-1]
        cv2_circle(
            image,
            (
                int(gaze_position[0]),
                int(gaze_position[1]),
            ),
            20,  # Circle radius
            (0, 0, 255),  # Color in BGR
            3,  # Circle thickness
        )
        return image


def main(args=None):
    # Initialize ROS DDS
    rclpy.init(args=args)
    glasses_publisher = pupilPublisher()

    try:
        rclpy.spin(glasses_publisher)
    except KeyboardInterrupt:
        glasses_publisher.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
