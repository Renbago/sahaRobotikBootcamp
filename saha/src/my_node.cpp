#include "saha/MyNode.hpp"

int main(int argc, char* argv[])
{
  rclcpp::init(argc, argv);
  auto node = std::make_shared<SahaNode>();
  rclcpp::executors::SingleThreadedExecutor executor;
  executor.add_node(node);
  executor.spin();

  // eğer ister HZ e ayarlayacaksanız:
    // while (rclcpp::ok()) {
        // // run check function with 10Hz
        // node->check();
        // rclcpp::spin_some(node);
        // std::this_thread::sleep_for(std::chrono::milliseconds(100));
    // }

  rclcpp::shutdown();
  return 0;
}
