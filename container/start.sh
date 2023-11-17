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

SCINTILLA_ROOT=''
get_script_parent_directory SCINTILLA_ROOT

if [ "${platform}" == "arm" ]; then
    info "Building for ARM platform..."
    docker run \
                --gpus all \
                --privileged \
                --platform="${PLATFORM}" \
                --hostname ${CONTAINER_NAME} \
                -v ${SCINTILLA_ROOT}:/sintilla \
                --name ${CONTAINER_NAME} \
                -itd ${IMAGE_NAME}
else
    error "Unsupported platform. Only 'arm' is supported for now."
    exit 1
fi
