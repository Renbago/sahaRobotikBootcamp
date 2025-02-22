FROM ros:humble

SHELL ["bash", "-c"]

ARG USERNAME=SahaRobotikEgitimls
RUN useradd -m -s /bin/bash $USERNAME && \
    echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers && \
    chown -R $USERNAME:$USERNAME /home/$USERNAME

USER $USERNAME
RUN echo "if [ -f /etc/bash_completion ]; then" >> ~/.bashrc && \
    echo "  . /etc/bash_completion" >> ~/.bashrc && \
    echo "fi" >> ~/.bashrc && \
    echo "source /opt/ros/humble/setup.bash" >> /home/$USERNAME/.bashrc && \
    echo 'source /home/'$USERNAME'/ros2_ws/devel/setup.bash' >> ~/.bashrc

WORKDIR /home/$USERNAME
CMD ["bash"]
