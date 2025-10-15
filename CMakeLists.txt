cmake_minimum_required(VERSION 3.5)
project(pupil_neon_ros)

# Default to C99
if(NOT CMAKE_C_STANDARD)
  set(CMAKE_C_STANDARD 99)
endif()

# Default to C++14
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find c++ dependencies
find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(rclpy REQUIRED)

find_package(builtin_interfaces REQUIRED)
find_package(std_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)

find_package(OpenCV REQUIRED) 
find_package(cv_bridge REQUIRED)

# Custom messages
find_package(rosidl_default_generators REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/Eye.msg"
  "msg/GazeData.msg"
  "msg/GazeEvent.msg"
  DEPENDENCIES builtin_interfaces std_msgs geometry_msgs sensor_msgs
 )

#Path to scripts
# ament_python_install_package(scripts)

install(PROGRAMS
  scripts/async_pupil_publisher.py
  scripts/rviz_visualizer.py
  # scripts/emulator_publisher.py
  # scripts/frame_publisher.py
  # scripts/pupil_publisher.py
  DESTINATION lib/${PROJECT_NAME}
)

# Path to resources
install(DIRECTORY
  launch
  DESTINATION share/${PROJECT_NAME}/
)

# install config files
install(DIRECTORY
  config
  DESTINATION share/${PROJECT_NAME}
)


if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # uncomment the line when a copyright and license is not present in all source files
  # set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # uncomment the line when this package is not in a git repo
  # set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
