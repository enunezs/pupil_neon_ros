#! /usr/bin/env python3

# GNU V3.0
# Copyright: Emanuel Nunez Sardinha
# URL:

## TODO: Add buffer to keep stracting frames from webcam

# * Core ROS dependencies
import rclpy
from rclpy.node import Node  #

# * Image messaging and conversion
from cv_bridge import CvBridge
import cv2  # TODO: specify particular modules of cv2
import numpy as np

# * Mouse emulation
import pyautogui

# * Base messages
from sensor_msgs.msg import Image
from geometry_msgs.msg import PointStamped

### Settings ###
### * DEBUG * ###
print_performance = False


class emulatorPublisher(Node):

    def __init__(self):
        super().__init__("glasses_emulator_node")
        self.get_logger().info("Glasses Emulator Node is Running...")

        # * Intialize publishers
        self.publisher_front_camera = self.create_publisher(
            Image, "pupil_glasses/front_camera", 1
        )
        self.publisher_gaze_position = self.create_publisher(
            PointStamped, "pupil_glasses/gaze_position", 1
        )

        # Declare and retrieve parameters
        self.camera_id = self.declare_and_get_parameter("camera_id", 1)
        self.publish_freq = self.declare_and_get_parameter("publish_freq", 30)
        self.draw_circle = self.declare_and_get_parameter("draw_circle", False)
        self.camera_depth = self.declare_and_get_parameter("camera_depth", 1.0)
        self.video_resolution = self.declare_and_get_parameter(
            "video_resolution", (1600, 1200)
        )

        # * Connect to webcam
        self.get_logger().info("Emulating glasses")
        self.bridge = CvBridge()
        self.get_logger().info(f"Connecting to webcam {self.camera_id}...")

        self.cap = cv2.VideoCapture(self.camera_id)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        # * Check if connection is succesful
        if self.cap == False:
            self.get_logger().info("Error opening video stream")
        else:
            self.get_logger().info("Video stream opened")

        # * Create publisher
        self.timer = self.create_timer(
            1.0 / self.publish_freq, self.publish_emulator_data
        )

        # * Init frame buffer
        self.frame_buffer = None

        # * Init debug vars
        self.iterations = 0
        self.total_time = 0

    def declare_and_get_parameter(self, name, default):
        self.declare_parameter(name, default)
        self.get_logger().info(
            f"Loaded parameter {name}: {self.get_parameter(name).value}"
        )
        return self.get_parameter(name).value

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
        ret, frame = self.cap.read()
        if ret:
            self.frame_buffer = frame
        else:
            if not self.frame_buffer:
                return
            frame = self.frame_buffer

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
        self.publisher_camera_info.publish(camera_info_msg)

        # * Calculate time difference between iterations and frame rate
        end_time = self.get_clock().now()

        if print_performance:
            self.print_performance_stats(start_time, end_time)

    # Get mouse coordinates as fimctopm of screen size
    def emulate_glasses(self):
        # Get screen size
        screen_res_x, screen_res_y = pyautogui.size()
        cursor_x, cursor_y = pyautogui.position()
        gaze_x, gaze_y = cursor_x / screen_res_x, cursor_y / screen_res_y
        # ros_time = self.get_clock().now().nanoseconds/1e9
        # ts = ros_time + 500000
        # pts = ros_time*0.09

        return (gaze_x, gaze_y)

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

        # Convert to uint8
        image = image.astype(np.uint8)
        # Apply Gaussian blur to remove noise -> Best left for receiver?
        # image = cv2.GaussianBlur(image, (5, 5), 0)

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
