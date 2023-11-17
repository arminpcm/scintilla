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

source settings.sh
source ../scripts/common_functions.sh
print_header

# Check args
check_args() {
    if [ "$#" -ne 1 ]; then
        error "Usage: $0 <platform>, platform can be arm or x86"
        exit 1
    fi
}

set -e

check_args $#

platform="$1"

set_container_variables $platform

if [ "${platform}" == "arm" ]; then
    info "Building for ARM platform..."
    docker build --build-arg L4T_MAJOR_VERSION=35 \
                 --build-arg L4T_MINOR_VERSION=2 \
                 --build-arg L4T_PATCH_VERSION=1 \
                 --build-arg ZED_SDK_MAJOR=4 \
                 --build-arg ZED_SDK_MINOR=0 \
                 --build-arg JETPACK_MAJOR=5 \
                 --build-arg JETPACK_MINOR=1.0 \
                 --build-arg L4T_BASE_IMAGE="l4t-jetpack" \
                 -f arm.dockerfile \
                 -t ${IMAGE_NAME} .
elif [ "${platform}" == "x86" ]; then
    info "Building for x86 platform..."
    docker build --build-arg UBUNTU_RELEASE_YEAR=22 \
                 --build-arg CUDA_MAJOR=12 \
                 --build-arg CUDA_MINOR=1.0 \
                 --build-arg ZED_SDK_MAJOR=4 \
                 --build-arg ZED_SDK_MINOR=0 \
                 -f dev.dockerfile \
                 -t ${IMAGE_NAME} .
else
    error "Unsupported platform. Only 'arm' and 'x86' are supported."
    exit 1
fi
