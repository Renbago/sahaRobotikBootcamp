#include "rviz_tools/robot_pose_publisher_tool.h"
#include <pluginlib/class_list_macros.hpp>

namespace robot_pose_tool
{

RobotPosePublisherTool::RobotPosePublisherTool()
{
  shortcut_key_ = 'p';
}

void RobotPosePublisherTool::onInitialize()
{
  auto ros_node_abstraction = context_->getRosNodeAbstraction().lock();
  if (!ros_node_abstraction) {
    RCLCPP_ERROR(rclcpp::get_logger("rviz_tools"), "ROS node abstraction is not available!");
    return;
  }
  node_ = ros_node_abstraction->get_raw_node();

  pose_pub_ = node_->create_publisher<geometry_msgs::msg::PoseWithCovarianceStamped>("save_table_mode", 10);
  pose_sub_ = node_->create_subscription<geometry_msgs::msg::PoseWithCovarianceStamped>(
    "amcl_pose", 10,
    std::bind(&RobotPosePublisherTool::poseCallback, this, std::placeholders::_1));
}

void RobotPosePublisherTool::poseCallback(const geometry_msgs::msg::PoseWithCovarianceStamped::SharedPtr msg)
{
  latest_pose_ = *msg;
}

int RobotPosePublisherTool::processMouseEvent(rviz_common::ViewportMouseEvent & event)
{
  if (event.leftUp()) {
    Ogre::Vector3 position;
    if (context_->getViewPicker()->get3DPoint(event.panel, event.x, event.y, position)) {
      geometry_msgs::msg::PoseStamped clicked_pose;
      clicked_pose.header.stamp = node_->get_clock()->now();
      clicked_pose.header.frame_id = "map"; 

      clicked_pose.pose.position.x = position.x;
      clicked_pose.pose.position.y = position.y;
      clicked_pose.pose.position.z = 0.0;
      clicked_pose.pose.orientation.w = 1.0;

      pose_pub_->publish(latest_pose_);

      RCLCPP_INFO(node_->get_logger(), "Published clicked pose at (%.2f, %.2f)", position.x, position.y);

      return Finished;  // Tool otomatik devreden çıkar
    } else {
      RCLCPP_WARN(node_->get_logger(), "No valid 3D point under mouse");
    }
  }

  return 0;
}

void RobotPosePublisherTool::activate()
{
  if (latest_pose_.header.frame_id.empty()) {
    RCLCPP_WARN(node_->get_logger(), "No valid pose received yet, cannot publish.");
    return;
  }
  RCLCPP_INFO(node_->get_logger(), "Tool activated, publishing current robot pose.");
  pose_pub_->publish(latest_pose_);
}

void RobotPosePublisherTool::deactivate()
{
  RCLCPP_INFO(node_->get_logger(), "Tool deactivated.");
}

} // namespace robot_pose_tool

PLUGINLIB_EXPORT_CLASS(robot_pose_tool::RobotPosePublisherTool, rviz_common::Tool)