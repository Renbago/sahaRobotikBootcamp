#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PointStamped, PoseStamped, PoseWithCovarianceStamped
from nav2_msgs.action import NavigateToPose
from rclpy.action import ActionClient
from robot_msgs.srv import StartTableMode

class ClickedPointSubscriber(Node):
    def __init__(self):
        super().__init__('clicked_point_listener')

        # `/clicked_point` konusunu dinle
        self.subscription = self.create_subscription(
            PointStamped,
            'clicked_point',
            self.point_callback,
            10)

        self.subscription = self.create_subscription(
            PoseWithCovarianceStamped,
            'save_table_mode',
            self.saved_table_mode_callback,
            10)

        # Hedef listesi
        self.waypoints_point = []
        self.waypoints_saved = []
        self.is_navigating = False 
        self.is_table_mode = False
        self.table_id_goal = False
        self.table_id = None

        self.start_table_mode_service = self.create_service(
            StartTableMode,
            'start_table_mode',
            self.start_table_mode_callback)
        
        self.navigate_to_saved_goal_service = self.create_service(
            StartTableMode,
            'navigate_to_saved_goal',
            self.navigate_to_saved_goal)

        self.nav_to_pose_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')

        self.get_logger().info("Clicked Point Subscriber Başladı. RViz'de hedef noktalar belirleyin.")

    def point_callback(self, msg):
        x, y = msg.point.x, msg.point.y
        self.waypoints_point.append((x, y))
        self.get_logger().info(f"Yeni Nokta Alındı: ({x}, {y})")

        if not self.is_navigating:
            self.navigate_to_next_goal()

    def saved_table_mode_callback(self, msg):
        """Kaydedilmiş noktaları al ve hedef listesine ekle."""

        if not self.is_table_mode:
            self.get_logger().info("Masa kaydetme modu etkin değil. Nokta kaydedilmiyor.")
            return

        x, y = msg.pose.pose.position.x, msg.pose.pose.position.y
        self.waypoints_saved.append((x, y))
        self.get_logger().info(f"Kaydedilmiş Nokta Alındı: ({x}, {y})")


    def start_table_mode_callback(self, req, res):
        """Kaydedilmiş noktaları al ve hedef listesine ekle."""
        self.is_table_mode = req.save_table_mode
        if self.is_table_mode:
            self.get_logger().info("Masa kaydetme modu etkinleştirildi.")
        else:
            self.get_logger().info("Masa kaydetme modu devre dışı bırakıldı.")

        res.success = True
        self.is_navigating = False
        return res

    def navigate_to_saved_goal(self, req, res):
        """Kaydedilmiş hedefe git."""
        self.table_id = req.table_id
        self.is_navigating = False
        
        if not self.is_navigating and not self.is_table_mode:
            self.table_id_goal = True
            self.navigate_to_next_goal()
            res.success = True
            return res
        else:
            self.get_logger().info("Navigasyon devam ediyor veya tablo modu etkin değil.")
            self.table_id_goal = False
            res.success = False
            return res


    def navigate_to_next_goal(self):
        """Sıradaki hedefe git."""
        if self.table_id_goal:
            if not self.waypoints_saved:
                self.get_logger().info("Kaydedilmiş hedef listesi boş. Beklemede...")
                self.is_navigating = False
                return

            # table_id index kontrolü
            if self.table_id >= len(self.waypoints_saved):
                self.get_logger().error(
                    f"Geçersiz table_id: {self.table_id}. Kayıtlı nokta sayısı: {len(self.waypoints_saved)}"
                )
                self.is_navigating = False
                return

            # Geçerli table_id → ilgili noktayı al
            x, y = self.waypoints_saved[self.table_id]
            self.get_logger().info(f"Table ID {self.table_id} ile hedef: ({x}, {y})")
        else:
            # Eski davranış (sırayla gidiyor)
            if not self.waypoints_point:
                self.get_logger().info("Hedef listesi boş. Beklemede...")
                self.is_navigating = False
                return

            x, y = self.waypoints_point.pop(0)


        self.is_navigating = True 
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
            self.get_logger().info("Hedef reddedildi!")
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
            self.is_navigating = False
        else:
            self.get_logger().info(f"Hedef başarısız oldu! Status Code: {result.status}")

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