cmake_minimum_required(VERSION 3.5)
project(rviz_tools)

if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 17)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(rviz_common REQUIRED)
find_package(rviz_default_plugins REQUIRED)
find_package(pluginlib REQUIRED)
find_package(Qt5 REQUIRED COMPONENTS Widgets Core Gui)

set(CMAKE_AUTOMOC ON)
set(CMAKE_INCLUDE_CURRENT_DIR ON)

set(plugin_headers
  include/rviz_tools/robot_pose_publisher_tool.h
)

qt5_wrap_cpp(moc_files ${plugin_headers})


include_directories(
  include
  ${rviz_common_INCLUDE_DIRS}
)

add_library(${PROJECT_NAME} SHARED
  src/robot_pose_publisher_tool.cpp
  ${moc_files}
)


target_link_libraries(${PROJECT_NAME}
  rclcpp::rclcpp
  geometry_msgs::geometry_msgs__rosidl_generator_cpp
  rviz_common::rviz_common
  pluginlib::pluginlib
  Qt5::Widgets
  Qt5::Core
  Qt5::Gui
)

ament_target_dependencies(${PROJECT_NAME}
  rclcpp
  geometry_msgs
  rviz_common
  rviz_default_plugins
  pluginlib
)

pluginlib_export_plugin_description_file(rviz_common plugin_description.xml)

install(TARGETS ${PROJECT_NAME}
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION bin
)

install(DIRECTORY include/
  DESTINATION include/${PROJECT_NAME}
)

install(FILES plugin_description.xml
  DESTINATION share/${PROJECT_NAME}
)

ament_export_include_directories(include)
ament_export_libraries(${PROJECT_NAME})
ament_export_dependencies(
  rclcpp
  geometry_msgs
  rviz_common
  rviz_default_plugins
  pluginlib
  Qt5
)

ament_package()