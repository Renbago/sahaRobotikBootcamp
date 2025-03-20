#!/usr/bin/env python3

import sys
import termios
import tty
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class SahaNode(Node):
    def __init__(self):
        super().__init__('saha_node')
        self.running = True

        # `cmd_vel` konusuna yayın yapacak publisher
        self.turtlebot_twist_pub = self.create_publisher(Twist, 'cmd_vel', 10)

        self.get_logger().info("Keyboard teleop started. Use W/A/S/D keys to move, X to stop, Q to quit.")

    def getch(self):
        """Tek bir karakter girişi almak için fonksiyon"""
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    def keyboard_loop(self):
        """Klavyeden girdiyi sürekli okuyan fonksiyon"""
        while self.running and rclpy.ok():
            try:
                c = self.getch()
            except Exception as e:
                self.get_logger().error(f"Klavye girdisi hatası: {e}")
                continue

            twist_msg = Twist()

            if c.lower() == 'w':  # İleri git
                twist_msg.linear.x = 1.0
            elif c.lower() == 's':  # Geri git
                twist_msg.linear.x = -1.0
            elif c.lower() == 'a':  # Sola dön
                twist_msg.angular.z = 1.0
            elif c.lower() == 'd':  # Sağa dön
                twist_msg.angular.z = -1.0
            elif c.lower() == 'x':  # Reset (Durdurma)
                twist_msg.linear.x = 0.0
                twist_msg.angular.z = 0.0
                self.get_logger().info("Robot durduruldu (Reset).")
            elif c.lower() == 'q':  # Çıkış yap
                self.get_logger().info("Exiting teleop.")
                self.running = False
                rclpy.shutdown()
                break
            else:
                continue  # Geçersiz tuş basıldıysa, hareketi güncelleme

            # Hareket komutunu yayınla
            self.turtlebot_twist_pub.publish(twist_msg)

def main(args=None):
    rclpy.init(args=args)
    node = SahaNode()
    
    try:
        node.keyboard_loop()  # Klavyeden veri almak için sürekli çalıştır
    except KeyboardInterrupt:
        node.get_logger().info("Kullanıcı tarafından durduruldu.")
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
