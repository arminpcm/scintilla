#!/bin/bash

################################################################################
# Title: Setup the host computer for development
# 
# Copyright (c) 2023 Scintilla. All rights reserved.
#
# The contents of this script are proprietary and confidential. Unauthorized
# reproduction, distribution, or disclosure of this material is strictly
# prohibited without the express written permission of Scintilla.
#
################################################################################

source scripts/common_functions.sh
print_header

set -e

# Update package list
sudo apt update

# Install QEMU to simulate ARM for development
sudo apt install -y qemu
info "QEMU has been successfully installed."

# Setup the environment variables

# Check if SCINTILLA_ROOT is set
if [ -z "$SCINTILLA_ROOT" ]; then
    SCINTILLA_ROOT=''
    get_script_parent_directory SCINTILLA_ROOT

    info "SCINTILLA_ROOT is not set. Setting it to $SCINTILLA_ROOT."

    # Add the command to set SCINTILLA_ROOT to 'Hello' in the shell configuration file
    echo "export SCINTILLA_ROOT=$SCINTILLA_ROOT" >> ~/.bashrc

    # Load the updated configuration
    warning "Run 'source ~/.bashrc' or restart your terminal to apply changes."
else
    warning "SCINTILLA_ROOT is already set to '$SCINTILLA_ROOT'."
fi
