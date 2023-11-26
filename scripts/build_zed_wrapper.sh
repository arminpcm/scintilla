#!/bin/bash

################################################################################
# Title: Builds the ROS2 wrapper for stereo zed camera
# 
# Copyright (c) 2023 Scintilla. All rights reserved.
#
# The contents of this script are proprietary and confidential. Unauthorized
# reproduction, distribution, or disclosure of this material is strictly
# prohibited without the express written permission of Scintilla.
#
################################################################################

source scripts/common_functions.sh
print_header

set -e

source /opt/ros/iron/setup.bash
sudo chown -R docker /thirdparty/*
sudo chown -R docker /usr/local/zed
cd /thirdparty/ros2_ws
source /opt/ros/iron/setup.sh
sudo rosdep init
rosdep update
rosdep install --from-paths src --ignore-src --rosdistro iron -r -y
colcon build --symlink-install --cmake-args=-DCMAKE_BUILD_TYPE=Release
echo "source /thirdparty/ros2_ws/install/local_setup.bash" >> ~/.bashrc
warning "Please run source ~/.bashrc command in your terminal"

