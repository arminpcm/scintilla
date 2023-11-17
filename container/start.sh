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

source ../scripts/common_functions.sh
print_header

set -e

SCINTILLA_ROOT=''
get_script_parent_directory SCINTILLA_ROOT
CONTAINER_NAME="scintilla"
IMAGE_NAME="scintilla:devel-l4t-r35.2"
HOSTNAME="scintilla"

docker run --gpus all --privileged --platform=linux/arm64 --hostname ${HOSTNAME} -v ${SCINTILLA_ROOT}:/sintilla --name ${CONTAINER_NAME} -itd ${IMAGE_NAME}
