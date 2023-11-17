#!/bin/bash

################################################################################
# Title: Setup the host computer for development
# 
# Copyright (c) 2023 Scintilla. All rights reserved.
#
# The contents of this script are proprietary and confidential. Unauthorized
# reproduction, distribution, or disclosure of this material is strictly
# prohibited without the express written permission of Scintilla.
#
################################################################################

# Exit on an error
set -e

# Import utility functions
source common_functions.sh

check_root

# Update package list
apt update

# Install QEMU to simulate ARM for development
apt install -y qemu
info "QEMU has been successfully installed."
