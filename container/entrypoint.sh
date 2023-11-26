#!/bin/bash

################################################################################
# Title: Container entrypoint commands
# 
# Copyright (c) 2023 Scintilla. All rights reserved.
#
# The contents of this script are proprietary and confidential. Unauthorized
# reproduction, distribution, or disclosure of this material is strictly
# prohibited without the express written permission of Scintilla.
#
################################################################################

# Source ROS2
echo "source /opt/ros/iron/setup.bash" >> ~/.bashrc
echo "source /home/.prompt.sh && export PS1=\"\$(__mkps1)\"" >> ~/.bashrc
echo "export SCINTILLA_ROOT=/scintilla" >> ~/.bashrc
echo "export PYTHONPATH=$PYTHONPATH:$SCINTILLA_ROOT/modules" >> ~/.bashrc
source ~/.bashrc
