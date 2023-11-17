#!/bin/bash

################################################################################
# Title: Dive intot the running docker image
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

CONTAINER_NAME="scintilla"

docker exec -it ${CONTAINER_NAME} /bin/bash
