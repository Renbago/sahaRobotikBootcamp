#pragma once

#ifndef SAHA_ROBOTIK_BOOTCAMP__MY_NODE_HPP_
#define SAHA_ROBOTIK_BOOTCAMP__MY_NODE_HPP_

#include <rclcpp/rclcpp.hpp>
#include <geometry_msgs/msg/twist.hpp>
#include <thread>
#include <atomic>
#include <termios.h>
#include <unistd.h>
#include <iostream>
#include <functional>

class SahaNode : public rclcpp::Node {
public:
    SahaNode();
    ~SahaNode();
        
private:
    void keyboardLoop();

    rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr turtlebot_twist_pub_;

    std::thread keyboard_thread_;

    std::atomic_bool running_;
};

#endif  // SAHA_ROBOTIK_BOOTCAMP__MY_NODE_HPP_

