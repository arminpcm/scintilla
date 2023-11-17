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
    docker build --build-arg L4T_MAJOR_VERSION=${L4T_MAJOR_VERSION} \
                 --build-arg L4T_MINOR_VERSION=${L4T_MINOR_VERSION} \
                 --build-arg L4T_PATCH_VERSION=${L4T_PATCH_VERSION} \
                 --build-arg ZED_SDK_MAJOR=${ZED_SDK_MAJOR} \
                 --build-arg ZED_SDK_MINOR=${ZED_SDK_MINOR} \
                 --build-arg JETPACK_MAJOR=${JETPACK_MAJOR} \
                 --build-arg JETPACK_MINOR=${JETPACK_MINOR} \
                 --build-arg L4T_BASE_IMAGE=${L4T_BASE_IMAGE} \
                 -f arm.dockerfile \
                 -t ${IMAGE_NAME} .
elif [ "${platform}" == "x86" ]; then
    info "Building for x86 platform..."
    docker build --build-arg UBUNTU_RELEASE_YEAR=${UBUNTU_RELEASE_YEAR} \
                 --build-arg CUDA_MAJOR=${CUDA_MAJOR} \
                 --build-arg CUDA_MINOR=${CUDA_MINOR} \
                 --build-arg ZED_SDK_MAJOR=${ZED_SDK_MAJOR} \
                 --build-arg ZED_SDK_MINOR=${ZED_SDK_MINOR} \
                 -f dev.dockerfile \
                 -t ${IMAGE_NAME} .
else
    error "Unsupported platform. Only 'arm' and 'x86' are supported."
    exit 1
fi
