#!/bin/bash

################################################################################
# Title: Build the docker image for dev
# 
# Copyright (c) 2023 Scintilla. All rights reserved.
#
# The contents of this script are proprietary and confidential. Unauthorized
# reproduction, distribution, or disclosure of this material is strictly
# prohibited without the express written permission of Scintilla.
#
################################################################################

# Exit on an error

source ../scripts/common_functions.sh
print_header

set -e

IMAGE_NAME="scintilla:devel-l4t-r35.2"

docker build --build-arg L4T_MAJOR_VERSION=35 \
             --build-arg L4T_MINOR_VERSION=2 \
             --build-arg L4T_PATCH_VERSION=1 \
             --build-arg ZED_SDK_MAJOR=4 \
             --build-arg ZED_SDK_MINOR=0 \
             --build-arg JETPACK_MAJOR=5 \
             --build-arg JETPACK_MINOR=1.0 \
             --build-arg L4T_BASE_IMAGE="l4t-jetpack" \
             -f dev.dockerfile \
             -t ${IMAGE_NAME} .
