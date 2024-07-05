#! /usr/bin/env python3

# GNU V3.0
# Copyright: Emanuel Nunez Sardinha
# URL:

## TODO: Add buffer to keep stacking frames from webcam

# * Core ROS dependencies
import rclpy
from rclpy.node import Node  #

# * Image messaging and conversion
from cv_bridge import CvBridge
import cv2  # TODO: specify particular modules of cv2
import numpy as np
import threading
import queue


# * Mouse emulation
import pyautogui

# * Base messages
from sensor_msgs.msg import Image
from geometry_msgs.msg import PointStamped


class emulatorPublisher(Node):

    def __init__(self):
        super().__init__("glasses_emulator_node")
        self.get_logger().info("Glasses Emulator Node is Running...")

        ### * Intialize publishers
        self.publisher_front_camera = self.create_publisher(
            Image, "pupil_glasses/front_camera/image_color", 1
        )
        self.publisher_camera_info = self.create_publisher(
            CameraInfo, "pupil_glasses/front_camera/camera_info", 1
        )
        self.publisher_gaze_position = self.create_publisher(
            PointStamped, "pupil_glasses/gaze_position", 1
        )

        # * Declare and retrieve parameters
        self.camera_id = self.declare_and_get_parameter("camera_id", 0)
        self.publish_freq = self.declare_and_get_parameter("publish_freq", 30)
        self.draw_circle = self.declare_and_get_parameter("draw_circle", False)
        self.camera_depth = self.declare_and_get_parameter("camera_depth", 1.0)
        self.video_resolution = self.declare_and_get_parameter(
            "video_resolution", (1600, 1200)
        )
        self.print_performance = self.declare_and_get_parameter(
            "print_performance", False
        )

        # Prepare camera calibration message
        self.front_camera_info = self.load_camera_info()

        self.bridge = CvBridge()

        # Start the frame capture thread
        self.get_logger().info("Emulating glasses")
        self.get_logger().info(f"Connecting to webcam {self.camera_id}...")
        self.frame_queue = queue.Queue(maxsize=10)  # Adjust maxsize as needed
        self.capture_thread = threading.Thread(target=self.capture_frames)
        self.capture_thread.daemon = True
        self.capture_thread.start()

        # * Create publisher
        self.timer = self.create_timer(
            1.0 / self.publish_freq, self.publish_emulator_data
        )

        # * Init debug vars
        self.iterations = 0
        self.total_time = 0

    # * Helper functions
    def declare_and_get_parameter(self, name, default):
        self.declare_parameter(name, default)
        self.get_logger().info(
            f"Loaded parameter {name}: {self.get_parameter(name).value}"
        )
        return self.get_parameter(name).value

    def load_camera_info(self):
        # For later. Needs calibration of the webcam. For now, use default values
        front_camera_info = CameraInfo()
        front_camera_info.width = self.video_resolution[0]
        front_camera_info.height = self.video_resolution[1]
        front_camera_info.distortion_model = "plumb_bob"

        front_camera_info.k = [
            883.10398037,
            0.0,
            796.76508223,
            0.0,
            889.42718313,
            646.25149238,
            0.0,
            0.0,
            1.0,
        ]
        front_camera_info.d = [
            -0.28984511,
            0.08497217,
            -0.00134947,
            -0.00125141,
            -0.01016795,
        ]
        # TODO: Repeat for inner cameras, simply iterate over index

        front_camera_info.binning_x = 0
        front_camera_info.binning_y = 0
        front_camera_info.roi.x_offset = 0
        front_camera_info.roi.y_offset = 0
        front_camera_info.roi.height = 0
        front_camera_info.roi.width = 0
        front_camera_info.roi.do_rectify = False

        return front_camera_info

    # Open separate thread to capture frames from webcam
    def capture_frames(self):
        cap = cv2.VideoCapture(self.camera_id, cv2.CAP_V4L)  # Use V4L for Linux
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        if not cap:
            self.get_logger().info("Error opening video stream")
        else:
            self.get_logger().info("Video stream opened")

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            if not self.frame_queue.full():
                self.frame_queue.put(frame)
            else:
                # Discard the oldest frame (if needed)
                self.frame_queue.get()
                self.frame_queue.put(frame)

    # Get mouse coordinates as function of screen size
    def emulate_glasses(self):
        # Get screen size
        screen_res_x, screen_res_y = pyautogui.size()
        cursor_x, cursor_y = pyautogui.position()
        gaze_x, gaze_y = cursor_x / screen_res_x, cursor_y / screen_res_y

        return (gaze_x, gaze_y)

    def publish_emulator_data(self):

        start_time = self.get_clock().now()

        # * Get latest data stream
        # Emulated: Webcam + Mouse
        gaze_coordinates = self.emulate_glasses()

        # * Pack gaze position into message
        gaze_msg = PointStamped()
        gaze_msg.point.x, gaze_msg.point.y = gaze_coordinates
        gaze_msg.point.z = self.camera_depth
        gaze_msg.header.stamp = self.get_clock().now().to_msg()
        gaze_msg.header.frame_id = "pupil_glasses_frame"

        # * Get latest image frame
        if not self.frame_queue.empty():
            frame = self.frame_queue.get()
        else:
            return

        # * Adjust colour and resize image
        # frame = self.modify_image(frame, greyscale= greyscale , video_resolution = video_resolution)
        if self.draw_circle:
            # frame = self.draw_circle(frame, gaze_coordinates)
            pass
        # * Pack image into message
        img_msg = self.bridge.cv2_to_imgmsg(frame)
        img_msg.header.stamp = self.get_clock().now().to_msg()
        img_msg.header.frame_id = "pupil_glasses_frame"

        # * Publish the message
        self.publisher_front_camera.publish(img_msg)
        self.publisher_gaze_position.publish(gaze_msg)
        self.publisher_camera_info.publish(self.front_camera_info)

        # * Calculate time difference between iterations and frame rate
        end_time = self.get_clock().now()

        if self.print_performance:
            self.print_performance_stats(start_time, end_time)

    def print_performance_stats(self, start_time, end_time):
        self.iterations += 1
        self.total_time += (end_time - start_time).nanoseconds / 1000000000
        if self.iterations % 10 == 0:
            self.get_logger().info(
                f"Average time per iteration: {self.total_time/self.iterations} s"
            )
            self.iterations = 0
            self.total_time = 0

    def modify_image(self, image, greyscale=False, video_resolution=(960, 540)):
        # Resize selected image to given dimension
        if greyscale:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = cv2.resize(image, video_resolution)
        image = image.astype(np.uint8)

        return image

    # Draw circle on image given gaze position
    def draw_circle(self, image, gaze_position):
        image_size = image.shape[:2][::-1]
        # Draw circle at gaze position
        cv2.circle(
            image,
            (
                int(gaze_position[0] * image_size[0]),
                int(gaze_position[1] * image_size[1]),
            ),
            10,
            (0, 255, 0),
            -1,
        )
        # Draw circle at center of image
        cv2.circle(
            image, (int(image_size[0] / 2), int(image_size[1] / 2)), 10, (0, 0, 255), -1
        )
        # Draw line from gaze position to center of image
        cv2.line(
            image,
            (
                int(gaze_position[0] * image_size[0]),
                int(gaze_position[1] * image_size[1]),
            ),
            (int(image_size[0] / 2), int(image_size[1] / 2)),
            (0, 0, 255),
            2,
        )
        return image


# * Core
def main(args=None):
    rclpy.init(args=args)  # Initialize ROS DDS
    glasses_emulator_publisher = emulatorPublisher()  # Create instance of function

    try:
        rclpy.spin(glasses_emulator_publisher)  # prevents closure. Run until interrupt
    except KeyboardInterrupt:
        cv2.destroyAllWindows()
        glasses_emulator_publisher.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
