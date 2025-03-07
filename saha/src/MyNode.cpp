#include "saha/MyNode.hpp"

char getch() {
  char buf = 0;
  struct termios old = {0};
  if (tcgetattr(0, &old) < 0)
    perror("tcgetattr()");
  old.c_lflag &= ~ICANON;  // Satır modu kapatılır.
  old.c_lflag &= ~ECHO;    // Ekrana yazdırma kapatılır.
  old.c_cc[VMIN] = 1;
  old.c_cc[VTIME] = 0;
  if (tcsetattr(0, TCSANOW, &old) < 0)
    perror("tcsetattr ICANON");
  if (read(0, &buf, 1) < 0)
    perror("read()");
  old.c_lflag |= ICANON;
  old.c_lflag |= ECHO;
  if (tcsetattr(0, TCSADRAIN, &old) < 0)
    perror ("tcsetattr ~ICANON");
  return buf;
}

SahaNode::SahaNode() 
  : Node("saha_node"), running_(true)
{
  turtlebot_twist_pub_ = this->create_publisher<geometry_msgs::msg::Twist>("turtle1/cmd_vel", 10);
  
  keyboard_thread_ = std::thread(&SahaNode::keyboardLoop, this);
}

SahaNode::~SahaNode() {
  running_ = false;
  if (keyboard_thread_.joinable()) {
    keyboard_thread_.join();
  }
}

void SahaNode::keyboardLoop() {
  RCLCPP_INFO(this->get_logger(), "Keyboard teleop started. Use W/A/S/D keys to move, Q to quit.");
  
  while (running_ && rclcpp::ok()) {
    char c = getch();
    geometry_msgs::msg::Twist twist_msg;

    twist_msg.linear.x = 0.0;
    twist_msg.linear.y = 0.0;
    twist_msg.linear.z = 0.0;
    twist_msg.angular.x = 0.0;
    twist_msg.angular.y = 0.0;
    twist_msg.angular.z = 0.0;

    if (c == 'w' || c == 'W') {
      twist_msg.linear.x = 1.0;
    } else if (c == 's' || c == 'S') {
      twist_msg.linear.x = -1.0;
    } else if (c == 'a' || c == 'A') {
      twist_msg.angular.z = 1.0;
    } else if (c == 'd' || c == 'D') {
      twist_msg.angular.z = -1.0;
    } else if (c == 'q' || c == 'Q') {
      RCLCPP_INFO(this->get_logger(), "Exiting teleop.");
      rclcpp::shutdown();
      break;
    } else {
      continue; 
    }

    turtlebot_twist_pub_->publish(twist_msg);
  }
}