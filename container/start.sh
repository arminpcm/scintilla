#!/bin/bash

################################################################################
# Title: Start the dev docker container
# 
# Copyright (c) 2023 Scintilla. All rights reserved.
#
# The contents of this script are proprietary and confidential. Unauthorized
# reproduction, distribution, or disclosure of this material is strictly
# prohibited without the express written permission of Scintilla.
#
################################################################################

source $SCINTILLA_ROOT/container/settings.sh
source $SCINTILLA_ROOT/scripts/common_functions.sh
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
    info "Starting ARM docker..."
    docker run \
                --gpus all \
                --privileged \
                -v /dev/bus/usb:/dev/bus/usb \
                --platform="${PLATFORM}" \
                --hostname ${CONTAINER_NAME} \
                -v ${SCINTILLA_ROOT}:/scintilla \
                --runtime nvidia \
                -e DISPLAY \
                -v /tmp/.X11-unix/:/tmp/.X11-unix \
                --name ${CONTAINER_NAME} \
                -itd ${IMAGE_NAME}
elif [ "${platform}" == "x86" ]; then
    info "Starting x86 docker..."
    docker run \
                --gpus all \
                --privileged \
                --memory=20g \
                -v /dev/bus/usb:/dev/bus/usb \
                --platform="${PLATFORM}" \
                --hostname ${CONTAINER_NAME} \
                -v ${SCINTILLA_ROOT}:/scintilla \
                --runtime nvidia \
                -e DISPLAY \
                -v /tmp/.X11-unix/:/tmp/.X11-unix \
                --network host \
                --name ${CONTAINER_NAME} \
                -itd ${IMAGE_NAME}
else
    error "Unsupported platform. Only 'arm' and 'x86' are supported."
    exit 1
fi

docker exec ${CONTAINER_NAME} bash -c '/scintilla/container/entrypoint.sh'
