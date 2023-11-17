#!/bin/bash

################################################################################
# Title: Settings for the dev container
# 
# Copyright (c) 2023 Scintilla. All rights reserved.
#
# The contents of this script are proprietary and confidential. Unauthorized
# reproduction, distribution, or disclosure of this material is strictly
# prohibited without the express written permission of Scintilla.
#
################################################################################

# Variables used by scripts
IMAGE_NAME=""
CONTAINER_NAME=""
HOSTNAME=""
PLATFORM=""
ZED_SDK_MAJOR=4
ZED_SDK_MINOR=0

# Arm specific variabels
L4T_IMAGE_NAME="scintilla:devel-l4t-v1"
L4T_CONTAINER_NAME="scintilla-l4t"
L4T_HOSTNAME="scintilla-l4t"
L4T_PLATFORM="linux/arm64"

L4T_MAJOR_VERSION=35
L4T_MINOR_VERSION=2
L4T_PATCH_VERSION=1
JETPACK_MAJOR=5
JETPACK_MINOR=1.0
L4T_BASE_IMAGE="l4t-jetpack"

# X86 specific variables
DEV_IMAGE_NAME="scintilla:devel-dev-v1"
DEV_CONTAINER_NAME="scintilla-dev"
DEV_HOSTNAME="scintilla-dev"
DEV_PLATFORM="linux/amd64"

UBUNTU_RELEASE_YEAR=22
CUDA_MAJOR=12
CUDA_MINOR=1.0
