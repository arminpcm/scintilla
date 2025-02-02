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
    info "Attaching ARM docker..."
    docker exec -it ${CONTAINER_NAME} /bin/bash
elif [ "${platform}" == "x86" ]; then
    info "Attaching x86 docker..."
    docker exec -it ${CONTAINER_NAME} /bin/bash
else
    error "Unsupported platform. Only 'arm' and 'x86' are supported."
    exit 1
fi
