#!/usr/bin/env python3

import asyncio
import typing as T
import threading
from datetime import datetime

import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup

from sensor_msgs.msg import Image, CompressedImage, Imu

from geometry_msgs.msg import PointStamped, Quaternion, Vector3

import cv2
import numpy as np

from pupil_neon_pkg.msg import (
    GazeData,
    Eye,
    GazeEvent,
)

from std_msgs.msg import Header
from cv_bridge import CvBridge

from pupil_labs.realtime_api import (
    Device,
    Network,
    receive_gaze_data,
    receive_video_frames,
    receive_eye_events_data,
    receive_imu_data,
)

from pupil_labs.realtime_api.streaming import (  # noqa: E402
    BlinkEventData,
    FixationEventData,
)

# DONE: Add other sensors
# DONE: Add IMU: Good exercise
# DONE: Change message to compressed
# DONE: Fix blinks

# LOW: Add eye cameras
# ! TODO: Make external plotter for data
# ! TODO: Make recalibration service, use offset?

# TODO: Fix combined image, make combined image optional, disabled by default. Disable queues too.
# TODO: Document it
# TODO: Load params
# TODO: Reduce library dependencies


class PupilLabsROS2Node(Node):
    def __init__(self):
        super().__init__("pupil_labs_node")

        # Initialize CV Bridge
        self.bridge = CvBridge()

        # Create callback groups for async operations
        self.async_group = MutuallyExclusiveCallbackGroup()

        # Publishers
        self.front_image_pub = self.create_publisher(
            CompressedImage, "pupil_glasses/front_image", 10
        )
        self.overlay_image_pub = self.create_publisher(
            Image, "pupil_glasses/overlay_image", 2
        )
        self.gaze_data_pub = self.create_publisher(
            GazeData, "pupil_glasses/gaze_data", 5
        )
        self.gaze_position_pub = self.create_publisher(
            PointStamped, "pupil_glasses/gaze_position", 5
        )
        self.saccade_pub = self.create_publisher(
            GazeEvent, "pupil_glasses/event/saccade", 1
        )
        self.fixation_pub = self.create_publisher(
            GazeEvent, "pupil_glasses/event/fixation", 1
        )
        self.saccade_onset_pub = self.create_publisher(
            GazeEvent, "pupil_glasses/event/saccade_onset", 1
        )
        self.fixation_onset_pub = self.create_publisher(
            GazeEvent, "pupil_glasses/event/fixation_onset", 1
        )
        self.blink_pub = self.create_publisher(
            GazeEvent, "pupil_glasses/event/blink", 1
        )
        self.imu_pub = self.create_publisher(Imu, "pupil_glasses/imu", 5)

        # Pre-allocate messages
        self.gaze_point = PointStamped()
        self.gaze_msg = GazeData()
        self.gaze_msg.left_eye = Eye()
        self.gaze_msg.right_eye = Eye()

        # Control flags
        self.running = True
        self.device_connected = False

        # Start the async pupil labs connection in a separate thread
        self.pupil_thread = threading.Thread(target=self._run_pupil_async_loop)
        self.pupil_thread.daemon = True
        self.pupil_thread.start()

        self.get_logger().info("Pupil Labs ROS2 Node initialized")

    # On a separate thread, collect data
    def _run_pupil_async_loop(self):
        """Run the async pupil labs code in a separate thread"""
        try:
            asyncio.run(self._pupil_main())
        except Exception as e:
            self.get_logger().error(f"Error in pupil async loop: {e}")

    ### Pupil Neon Glasses ###
    # HEAVILY Based on async example from https://pupil-labs.github.io/pl-realtime-api/dev/methods/async/streaming/scene-camera/#scene-camera-video-with-overlayed-gaze

    async def _pupil_main(self):
        """Main async function for Pupil Labs connection"""

        ### Scan for devices
        async with Network() as network:
            dev_info = await network.wait_for_new_device(timeout_seconds=5)
        if dev_info is None:
            self.get_logger().error("No device could be found!")
            return

        ### Connect to device
        async with Device.from_discovered_device(dev_info) as device:
            self.get_logger().info(f"Connected to {device}")
            status = await device.get_status()

            # Check sensors
            sensor_gaze = status.direct_gaze_sensor()
            if not sensor_gaze.connected:
                self.get_logger().error("Gaze sensor not connected")
                return

            sensor_world = status.direct_world_sensor()
            if not sensor_world.connected:
                self.get_logger().error("Scene camera not connected")
                return

            sensor_eye_events = status.direct_eye_events_sensor()
            if not sensor_eye_events.connected:
                self.get_logger().error(
                    f"Eye events sensor is not connected to {device}"
                )
                return
            sensor_imu = status.direct_imu_sensor()
            if not sensor_imu.connected:
                print(f"Imu sensor is not connected to {device}")
                return

            restart_on_disconnect = True

            # Queues for sensor data
            self.queue_video = asyncio.Queue(maxsize=1)
            self.queue_gaze = asyncio.Queue(maxsize=4)
            self.queue_eye_events = asyncio.Queue(maxsize=3)
            self.queue_imu = asyncio.Queue(maxsize=3)

            self.device_connected = True
            self.get_logger().info("All sensors connected, starting data streams...")

            # Create async tasks for publishing lone sensors
            process_video = asyncio.create_task(
                self._enqueue_sensor_data(
                    receive_video_frames(
                        sensor_world.url, run_loop=restart_on_disconnect
                    ),
                    self.queue_video,
                    "video",
                )
            )
            process_gaze = asyncio.create_task(
                self._enqueue_sensor_data(
                    receive_gaze_data(sensor_gaze.url, run_loop=restart_on_disconnect),
                    self.queue_gaze,
                    "gaze",
                )
            )
            process_gaze_events = asyncio.create_task(
                self._enqueue_sensor_data(
                    receive_eye_events_data(
                        sensor_eye_events.url, run_loop=restart_on_disconnect
                    ),
                    self.queue_eye_events,
                    "gaze_events",
                )
            )
            process_imu = asyncio.create_task(
                self._enqueue_sensor_data(
                    receive_imu_data(sensor_imu.url, run_loop=restart_on_disconnect),
                    self.queue_imu,
                    "imu",
                )
            )

            # Processing task for assembled data
            # process_data = asyncio.create_task(self._process_and_publish())

            try:
                # Wait for tasks
                await asyncio.gather(
                    process_video,
                    process_gaze,
                    process_gaze_events,
                    process_imu,
                    # process_data,
                )
            finally:
                self.get_logger().info("Cancelling tasks...")
                process_video.cancel()
                process_gaze.cancel()
                process_gaze_events.cancel()
                process_imu.cancel()
                # process_data.cancel()

    async def _enqueue_sensor_data(
        self, sensor: T.AsyncIterator, queue: asyncio.Queue, sensor_type: str
    ):
        """Enqueue sensor data with type logging"""
        async for datum in sensor:
            if not self.running:
                break
            try:
                # store most recent data
                # queue.put_nowait((datum.datetime, datum))

                # TODO: publish most recent data here depending on sensor type
                # self.get_logger().info(f"Received {sensor_type} datum: {datum}")
                if sensor_type == "video":
                    # TODO compress and send
                    # Ensure proper numpy array creation
                    bgr_buffer = datum.to_ndarray(format="bgr24")
                    # Make sure it's a proper contiguous array
                    if not bgr_buffer.flags["C_CONTIGUOUS"]:
                        bgr_buffer = np.ascontiguousarray(bgr_buffer)
                    self._publish_front_image(bgr_buffer, datum.datetime)

                elif sensor_type == "gaze":
                    self._publish_gaze_data(datum)

                elif sensor_type == "gaze_events":
                    self._publish_gaze_events_data(datum)

                elif sensor_type == "imu":
                    self._publish_imu_data(datum)
                else:
                    self.get_logger().error(f"Unknown sensor type: {sensor_type}")

            except asyncio.QueueFull:
                self.get_logger().warn(f"{sensor_type} queue full, dropping data")

    # TODO: Should be optional
    async def _process_and_publish(self):
        """Process sensor data and publish to ROS topics"""
        while self.running and self.device_connected:
            try:
                # Get most recent video frame
                video_datetime, video_frame = await self._get_most_recent_item(
                    self.queue_video
                )

                # Get closest gaze data
                _, gaze_datum = await self._get_closest_item(
                    self.queue_gaze, video_datetime
                )

                # Convert video frame to numpy array
                bgr_buffer = video_frame.to_ndarray(format="bgr24").copy()

                if (
                    gaze_datum
                    and not np.isnan(gaze_datum.x)
                    and not np.isnan(gaze_datum.y)
                ):
                    # Ensure coordinates are within image bounds
                    x_coord = max(0, min(int(gaze_datum.x), bgr_buffer.shape[1] - 1))
                    y_coord = max(0, min(int(gaze_datum.y), bgr_buffer.shape[0] - 1))

                    # Draw gaze circle directly on the copied buffer
                    try:
                        cv2.circle(
                            bgr_buffer,
                            center=(x_coord, y_coord),
                            radius=40,
                            color=(0, 0, 255),
                            thickness=8,
                        )
                        self.get_logger().debug("Circle drawn successfully")

                    except Exception as circle_error:
                        self.get_logger().error(
                            f"OpenCV circle drawing failed: {circle_error}"
                        )

                        # Fallback: Draw manually using numpy indexing
                        try:
                            self.get_logger().info(
                                "Using manual circle drawing fallback..."
                            )

                            # Create owned buffer for manual drawing
                            height, width, channels = bgr_buffer.shape
                            manual_buffer = np.array(
                                bgr_buffer, copy=True, dtype=np.uint8
                            )

                            # Draw a simple filled circle manually
                            y_coords, x_coords = np.ogrid[:height, :width]
                            mask = (x_coords - x_coord) ** 2 + (
                                y_coords - y_coord
                            ) ** 2 <= 40**2

                            # Draw filled circle
                            manual_buffer[mask] = [0, 0, 255]  # Red in BGR

                            # Draw ring for thickness (keep inner part original)
                            inner_mask = (x_coords - x_coord) ** 2 + (
                                y_coords - y_coord
                            ) ** 2 <= 32**2
                            manual_buffer[inner_mask] = bgr_buffer[inner_mask]

                            bgr_buffer = manual_buffer
                            self.get_logger().debug("Manual circle drawing successful")

                        except Exception as manual_error:
                            self.get_logger().error(
                                f"Manual circle drawing failed: {manual_error}"
                            )
                            self.get_logger().error("Skipping gaze overlay completely")

                # Publish overlay image
                self._publish_overlay_image(bgr_buffer, video_datetime)

            except Exception as e:
                self.get_logger().error(f"Error processing data: {e}")
                await asyncio.sleep(0.001)

    ### Publishers ###
    def _publish_front_image(self, bgr_image, timestamp):
        """Publish raw image to ROS topic"""
        try:
            if not isinstance(bgr_image, np.ndarray):
                raise TypeError(f"Expected numpy.ndarray, got {type(bgr_image)}")
            if bgr_image is None:
                raise ValueError("bgr_image is None")

            # Ensure the array is contiguous and properly formatted for OpenCV
            if not bgr_image.flags["C_CONTIGUOUS"]:
                bgr_image = np.ascontiguousarray(bgr_image)

            # Ensure correct data type
            if bgr_image.dtype != np.uint8:
                bgr_image = bgr_image.astype(np.uint8)

            # Create a copy to ensure memory ownership
            bgr_image_copy = bgr_image.copy()

            self.get_logger().debug(
                f"Image shape: {bgr_image_copy.shape}, dtype: {bgr_image_copy.dtype}, contiguous: {bgr_image_copy.flags['C_CONTIGUOUS']}"
            )

            # Convert to compressed ROS2 image
            compressed_msg = self.bridge.cv2_to_compressed_imgmsg(
                bgr_image_copy, dst_format="jpg"
            )

            compressed_msg.header = self._create_header(timestamp)
            self.front_image_pub.publish(compressed_msg)
            self.get_logger().debug("Front image published successfully")

        except Exception as e:
            self.get_logger().error(f"Error publishing front image: {e}")

    def _publish_overlay_image(self, overlay_image, timestamp):
        """Publish overlay image to ROS topic"""
        try:
            ros_image = self.bridge.cv2_to_imgmsg(overlay_image, "bgr8")
            ros_image.header = self._create_header(timestamp)
            self.overlay_image_pub.publish(ros_image)
        except Exception as e:
            self.get_logger().error(f"Error publishing overlay image: {e}")

    def _publish_imu_data(self, imu_datum):
        try:
            imu_msg = Imu()
            imu_msg.header = self._create_header(imu_datum.datetime)
            imu_msg.orientation = Quaternion(
                x=imu_datum.quaternion.x,
                y=imu_datum.quaternion.y,
                z=imu_datum.quaternion.z,
                w=imu_datum.quaternion.w,
            )
            imu_msg.angular_velocity = Vector3(
                x=imu_datum.gyro_data.x,
                y=imu_datum.gyro_data.y,
                z=imu_datum.gyro_data.z,
            )
            imu_msg.linear_acceleration = Vector3(
                x=imu_datum.accel_data.x,
                y=imu_datum.accel_data.y,
                z=imu_datum.accel_data.z,
            )

            imu_msg.orientation_covariance[0] = -1
            imu_msg.angular_velocity_covariance[0] = -1
            imu_msg.linear_acceleration_covariance[0] = -1

            self.imu_pub.publish(imu_msg)

        except Exception as e:
            self.get_logger().error(f"Error publishing imu: {e}")

        pass

    def _publish_gaze_data(self, gaze_datum):
        """Publish gaze point to ROS topic"""
        try:
            # Create a PointStamped message
            self.gaze_point.header = self._create_header(gaze_datum.datetime)
            self.gaze_point.point.x = float(gaze_datum.x)
            self.gaze_point.point.y = float(gaze_datum.y)
            self.gaze_point.point.z = 0.0  # 2D gaze point
            self.gaze_position_pub.publish(self.gaze_point)

            # Create a GazeData message
            self.gaze_msg.header = self._create_header(gaze_datum.datetime)
            self.gaze_msg.x = float(gaze_datum.x)
            self.gaze_msg.y = float(gaze_datum.y)
            self.gaze_msg.worn = False

            self.gaze_msg.left_eye.pupil_diameter = float(
                gaze_datum.pupil_diameter_left
            )
            self.gaze_msg.left_eye.eyeball_center_x = float(
                gaze_datum.eyeball_center_left_x
            )
            self.gaze_msg.left_eye.eyeball_center_y = float(
                gaze_datum.eyeball_center_left_y
            )
            self.gaze_msg.left_eye.eyeball_center_z = float(
                gaze_datum.eyeball_center_left_z
            )
            self.gaze_msg.left_eye.optical_axis_x = float(
                gaze_datum.optical_axis_left_x
            )
            self.gaze_msg.left_eye.optical_axis_y = float(
                gaze_datum.optical_axis_left_y
            )
            self.gaze_msg.left_eye.optical_axis_z = float(
                gaze_datum.optical_axis_left_z
            )
            self.gaze_msg.left_eye.eyelid_angle_top = float(
                gaze_datum.eyelid_angle_top_left
            )
            self.gaze_msg.left_eye.eyelid_angle_bottom = float(
                gaze_datum.eyelid_angle_bottom_left
            )
            self.gaze_msg.left_eye.eyelid_aperture = float(
                gaze_datum.eyelid_aperture_left
            )

            self.gaze_msg.right_eye.pupil_diameter = float(
                gaze_datum.pupil_diameter_right
            )
            self.gaze_msg.right_eye.eyeball_center_x = float(
                gaze_datum.eyeball_center_right_x
            )
            self.gaze_msg.right_eye.eyeball_center_y = float(
                gaze_datum.eyeball_center_right_y
            )
            self.gaze_msg.right_eye.eyeball_center_z = float(
                gaze_datum.eyeball_center_right_z
            )
            self.gaze_msg.right_eye.optical_axis_x = float(
                gaze_datum.optical_axis_right_x
            )
            self.gaze_msg.right_eye.optical_axis_y = float(
                gaze_datum.optical_axis_right_y
            )
            self.gaze_msg.right_eye.optical_axis_z = float(
                gaze_datum.optical_axis_right_z
            )
            self.gaze_msg.right_eye.eyelid_angle_top = float(
                gaze_datum.eyelid_angle_top_right
            )
            self.gaze_msg.right_eye.eyelid_angle_bottom = float(
                gaze_datum.eyelid_angle_bottom_right
            )
            self.gaze_msg.right_eye.eyelid_aperture = float(
                gaze_datum.eyelid_aperture_right
            )

            self.gaze_data_pub.publish(self.gaze_msg)
        except Exception as e:
            self.get_logger().error(f"Error publishing gaze data: {e}")

    def _publish_gaze_events_data(self, gaze_events_datum):
        """Publish gaze events to ROS topic"""
        try:
            if not isinstance(gaze_events_datum, (FixationEventData, BlinkEventData)):
                return  # Ignore unsupported types

            # Build base message
            gaze_events_msg = GazeEvent()
            gaze_events_msg.header = self._create_header(gaze_events_datum.datetime)
            gaze_events_msg.event_type = gaze_events_datum.event_type
            gaze_events_msg.start_time_ns = gaze_events_datum.start_time_ns
            gaze_events_msg.rtp_ts_unix_seconds = gaze_events_datum.rtp_ts_unix_seconds

            # Map for single-field events (no gaze coords)
            early_publish_map = {
                2: self.fixation_onset_pub,  # fixation onset
                3: self.saccade_onset_pub,  # saccade onset
            }
            if gaze_events_msg.event_type in early_publish_map:
                early_publish_map[gaze_events_msg.event_type].publish(gaze_events_msg)
                self.get_logger().debug(f"Published event: {gaze_events_msg}")
                return

            # Common end time for later events
            gaze_events_msg.end_time_ns = gaze_events_datum.end_time_ns

            # Special blink handling (type check + event_type)
            if gaze_events_msg.event_type == 4 and isinstance(
                gaze_events_datum, BlinkEventData
            ):
                self.blink_pub.publish(gaze_events_msg)
                self.get_logger().debug(f"Published blink event: {gaze_events_msg}")
                return

            # Add gaze-related fields
            gaze_events_msg.start_gaze_x = gaze_events_datum.start_gaze_x
            gaze_events_msg.start_gaze_y = gaze_events_datum.start_gaze_y
            gaze_events_msg.end_gaze_x = gaze_events_datum.end_gaze_x
            gaze_events_msg.end_gaze_y = gaze_events_datum.end_gaze_y
            gaze_events_msg.mean_gaze_x = gaze_events_datum.mean_gaze_x
            gaze_events_msg.mean_gaze_y = gaze_events_datum.mean_gaze_y
            gaze_events_msg.amplitude_pixels = gaze_events_datum.amplitude_pixels
            gaze_events_msg.amplitude_angle_deg = gaze_events_datum.amplitude_angle_deg
            gaze_events_msg.mean_velocity = gaze_events_datum.mean_velocity
            gaze_events_msg.max_velocity = gaze_events_datum.max_velocity

            # Map for full gaze events
            full_publish_map = {
                1: self.fixation_pub,  # Fixation
                0: self.saccade_pub,  # Saccade
            }
            if gaze_events_msg.event_type in full_publish_map:
                full_publish_map[gaze_events_msg.event_type].publish(gaze_events_msg)
                self.get_logger().debug(f"Published event: {gaze_events_msg}")

        except Exception as e:
            self.get_logger().error(f"Error publishing gaze events data: {e}")

    def _create_header(self, timestamp):
        """Create ROS header from datetime"""
        header = Header()
        header.frame_id = "pupil_camera"

        # Convert datetime to ROS time
        unix_timestamp = timestamp.timestamp()
        header.stamp.sec = int(unix_timestamp)
        header.stamp.nanosec = int((unix_timestamp - int(unix_timestamp)) * 1e9)

        return header

    ### async QUEUEs
    async def _get_most_recent_item(self, queue):
        """Get most recent item from queue"""
        item = await queue.get()
        while True:
            try:
                next_item = queue.get_nowait()
                item = next_item
            except asyncio.QueueEmpty:
                return item

    async def _get_closest_item(self, queue, timestamp):
        """Get closest item to timestamp"""
        item_ts, item = await queue.get()
        if item_ts > timestamp:
            return item_ts, item

        while True:
            try:
                next_item_ts, next_item = queue.get_nowait()
            except asyncio.QueueEmpty:
                return item_ts, item
            else:
                if next_item_ts > timestamp:
                    return next_item_ts, next_item
                item_ts, item = next_item_ts, next_item

    ### ROS2
    def destroy_node(self):
        """Clean shutdown"""
        self.running = False
        # cv2.destroyAllWindows()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)

    node = PupilLabsROS2Node()
    executor = MultiThreadedExecutor()

    try:
        rclpy.spin(node, executor=executor)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
