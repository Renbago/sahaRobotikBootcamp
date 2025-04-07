#ifndef ROBOT_POSE_PUBLISHER_TOOL_H
#define ROBOT_POSE_PUBLISHER_TOOL_H

#include <geometry_msgs/msg/pose_with_covariance_stamped.hpp>
#include <rclcpp/rclcpp.hpp>
#include <rviz_common/tool.hpp>
#include <rviz_common/display_context.hpp>
#include <rviz_common/viewport_mouse_event.hpp>
#include <rviz_common/interaction/view_picker_iface.hpp>

namespace robot_pose_tool
{

class RobotPosePublisherTool : public rviz_common::Tool
{
Q_OBJECT
public:
  RobotPosePublisherTool();
  void onInitialize() override;
  void activate() override;
  void deactivate() override;
  int processMouseEvent(rviz_common::ViewportMouseEvent & event) override;

private:
  rclcpp::Node::SharedPtr node_;
  rclcpp::Publisher<geometry_msgs::msg::PoseWithCovarianceStamped>::SharedPtr pose_pub_;
  rclcpp::Subscription<geometry_msgs::msg::PoseWithCovarianceStamped>::SharedPtr pose_sub_;
  geometry_msgs::msg::PoseWithCovarianceStamped latest_pose_;

  void poseCallback(const geometry_msgs::msg::PoseWithCovarianceStamped::SharedPtr msg);
};

} // namespace robot_pose_tool

#endif // ROBOT_POSE_PUBLISHER_TOOL_H