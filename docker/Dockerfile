FROM osrf/ros:humble-desktop-full

ARG USERNAME=sahaRobotikBootcamp

SHELL ["bash", "-c"]

RUN useradd -m -s /bin/bash $USERNAME && \
    echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers && \
    chown -R $USERNAME:$USERNAME /home/$USERNAME

# Gerekli ROS paketlerini kurma
RUN apt-get update && apt-get install -y \
    ros-humble-turtlebot3* \
    sudo \
    ros-humble-nav2-bringup \
    ros-humble-navigation2 \
    ros-humble-rviz2 \
    ros-humble-tf2-sensor-msgs \
    ros-humble-geographic-msgs \
    ros-humble-cartographer \
    ros-humble-cartographer-ros \
    git \
    build-essential \
    cmake \
    && rm -rf /var/lib/apt/lists/*

RUN apt install cppzmq-dev ros-humble-ros-gz -y --no-install-recommends --no-install-suggests || true

USER $USERNAME
WORKDIR /home/$USERNAME

RUN echo "if [ -f /etc/bash_completion ]; then" >> ~/.bashrc && \
    echo "  . /etc/bash_completion" >> ~/.bashrc && \
    echo "fi" >> ~/.bashrc && \
    echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc && \
    echo "export TURTLEBOT3_MODEL=waffle" >> ~/.bashrc && \
    echo "source /usr/share/gazebo/setup.sh" >> ~/.bashrc && \
    echo "export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:/opt/ros/humble/share/turtlebot3_gazebo/models" >> ~/.bashrc && \
    echo "export ROS_LOCALHOST_ONLY=1" >> ~/.bashrc

CMD ["bash"]