#!/bin/bash

################################################################################
# Title: Stop the host computer for development
# 
# Copyright (c) 2023 Scintilla. All rights reserved.
#
# The contents of this script are proprietary and confidential. Unauthorized
# reproduction, distribution, or disclosure of this material is strictly
# prohibited without the express written permission of Scintilla.
#
################################################################################

source ../scripts/common_functions.sh
print_header

CONTAINER_NAME="scintilla"

# Check if the container is running
if docker ps -q --filter "name=${CONTAINER_NAME}" | grep -q .; then
    # Container is running, stop it
    if docker stop "${CONTAINER_NAME}" > /dev/null 2>&1; then
        info "Container ${CONTAINER_NAME} stopped successfully."
    else
        error "Unable to stop container: ${CONTAINER_NAME}"
    fi
else
    info "Container ${CONTAINER_NAME} is not running."
fi

# Check if the container exists
if docker ps -a -q --filter "name=${CONTAINER_NAME}" | grep -q .; then
    # Container exists, remove it
    if docker rm "${CONTAINER_NAME}" > /dev/null 2>&1; then
        info "Container ${CONTAINER_NAME} removed successfully."
    else
        error "Unable to remove container: ${CONTAINER_NAME}"
    fi
else
    info "Container ${CONTAINER_NAME} does not exist."
fi
