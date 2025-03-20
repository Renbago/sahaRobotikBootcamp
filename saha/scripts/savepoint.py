#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PointStamped, PoseStamped
from nav2_msgs.action import NavigateToPose
from rclpy.action import ActionClient

class ClickedPointSubscriber(Node):
    def __init__(self):
        super().__init__('clicked_point_listener')

        # `/clicked_point` konusunu dinle
        self.subscription = self.create_subscription(
            PointStamped,
            '/clicked_point',
            self.point_callback,
            10)
        
        # Hedef listesi
        self.waypoints = []
        self.is_navigating = False 

        self.nav_to_pose_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')

        self.get_logger().info("Clicked Point Subscriber Başladı. RViz'de hedef noktalar belirleyin.")

    def point_callback(self, msg):
        x, y = msg.point.x, msg.point.y
        self.waypoints.append((x, y))
        self.get_logger().info(f"Yeni Nokta Alındı: ({x}, {y})")

        if not self.is_navigating:
            self.navigate_to_next_goal()

    def navigate_to_next_goal(self):
        """Sıradaki hedefe git."""
        if not self.waypoints:
            self.get_logger().info("Hedef listesi boş. Beklemede...")
            self.is_navigating = False
            return
        
        self.is_navigating = True 
        x, y = self.waypoints.pop(0)  # İlk noktayı al ve listeden çıkar

        goal_msg = NavigateToPose.Goal()
        goal_msg.pose.header.frame_id = "map"
        goal_msg.pose.header.stamp = self.get_clock().now().to_msg()
        goal_msg.pose.pose.position.x = x
        goal_msg.pose.pose.position.y = y
        goal_msg.pose.pose.orientation.w = 1.0  # açı vermiyoruz.
        
        self.get_logger().info(f"Yeni hedefe gidiliyor: ({x}, {y})")
        
        self.nav_to_pose_client.wait_for_server()
        send_goal_future = self.nav_to_pose_client.send_goal_async(goal_msg)
        send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):

        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().warn("Hedef reddedildi!")
            self.is_navigating = False
            return
        
        self.get_logger().info("Hedef kabul edildi, robota gönderildi.")
        get_result_future = goal_handle.get_result_async()
        get_result_future.add_done_callback(self.goal_result_callback)

    def goal_result_callback(self, future):

        result = future.result()

        # why 4 ?  https://github.com/ros2/rclpy/blob/humble/rclpy/rclpy/action/client.py
        # https://github.com/ros-navigation/navigation2/blob/humble/nav2_msgs/action/NavigateToPose.action
        if result.status == 4:  # SUCCEEDED
            self.get_logger().info("Hedef başarıyla tamamlandı.")
        else:
            self.get_logger().warn(f"Hedef başarısız oldu! Status Code: {result.status}")

        # Bir sonraki hedefe git
        self.navigate_to_next_goal()

def main(args=None):
    rclpy.init(args=args)
    node = ClickedPointSubscriber()
    rclpy.spin(node)  
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
