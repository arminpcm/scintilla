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

################################################################################
# Install docker
################################################################################
# Add Docker's official GPG key:
sudo apt update
info "Installing docker dependencies"
sudo apt install ca-certificates curl gnupg

info "Adding docker's GPG key"
sudo install -m 0755 -d /etc/apt/keyrings
sudo rm /etc/apt/keyrings/docker.gpg
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update

# Install the latest version
info "Installing docker"
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Add docker to the user groups
info "Setting up user group"
group_name="docker"

if ! getent group "$group_name" > /dev/null; then
    sudo groupadd "$group_name"
    info "Group '$group_name' added successfully."
    sudo usermod -aG docker $USER
else
    info "Group '$group_name' already exists."
fi

warning "You may need to restart your computer to continue"
# Verify
docker run hello-world

################################################################################
# Install QEMU to simulate ARM for development
################################################################################
info "Installing QEMU"
sudo apt install -y qemu
info "QEMU has been successfully installed."

# Setup the environment variables
# Check if SCINTILLA_ROOT is set
info "Setting up repository root environment variable"
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

################################################################################
# Install Airflow
################################################################################
if [ -z "$AIRFLOW_HOME" ]; then
    info "AIRFLOW_HOME is not set. Setting it to $SCINTILLA_ROOT/data/airflow."

    # Add the command to set SCINTILLA_ROOT to 'Hello' in the shell configuration file
    echo "export AIRFLOW_HOME=$SCINTILLA_ROOT/data/airflow" >> ~/.bashrc

    # Load the updated configuration
    warning "Run 'source ~/.bashrc' or restart your terminal to apply changes."
else
    warning "AIRFLOW_HOME is already set to '$AIRFLOW_HOME'."
fi

export AIRFLOW_HOME=$SCINTILLA_ROOT/data/airflow
AIRFLOW_VERSION=2.7.3
# Extract the version of Python you have installed. If you're currently using a Python version that is not supported by Airflow, you may want to set this manually.
# See above for supported versions.
PYTHON_VERSION="$(python3 --version | cut -d " " -f 2 | cut -d "." -f 1-2)"
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
