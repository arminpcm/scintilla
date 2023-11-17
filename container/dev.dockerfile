################################################################################
# Dockerfile for Scintilla
# Copyright (c) 2023 Scintilla. All rights reserved.
#
# This Dockerfile is private and confidential. Unauthorized copying or
# reproduction of this file, via any medium, is strictly prohibited without
# the explicit permission of Scintilla.
#
################################################################################

ARG UBUNTU_RELEASE_YEAR
ARG CUDA_MAJOR
ARG CUDA_MINOR

FROM nvidia/cudagl:${CUDA_MAJOR}.${CUDA_MINOR}-devel-ubuntu${UBUNTU_RELEASE_YEAR}.04

ARG UBUNTU_RELEASE_YEAR
ARG CUDA_MAJOR
ARG CUDA_MINOR
ARG ZED_SDK_MAJOR
ARG ZED_SDK_MINOR

ENV NVIDIA_DRIVER_CAPABILITIES \
    ${NVIDIA_DRIVER_CAPABILITIES:+$NVIDIA_DRIVER_CAPABILITIES,}compute,video,utility,graphics

RUN echo "Europe/Paris" > /etc/localtime ; echo "CUDA Version ${CUDA_MAJOR}.${CUDA_MINOR}.0" > /usr/local/cuda/version.txt

# Setup the ZED SDK
RUN apt-get update -y || true ; apt-get install --no-install-recommends lsb-release wget less udev zstd sudo build-essential cmake python3 python3-pip libpng-dev libgomp1 -y ; \
    #python3 -m pip install --upgrade pip ; \
    python3 -m pip install numpy opencv-python pyopengl ; \
    wget -q -O ZED_SDK_Linux_Ubuntu${UBUNTU_RELEASE_YEAR}.run https://download.stereolabs.com/zedsdk/${ZED_SDK_MAJOR}.${ZED_SDK_MINOR}/cu${CUDA_MAJOR}${CUDA_MINOR%.*}/ubuntu${UBUNTU_RELEASE_YEAR} && \
    chmod +x ZED_SDK_Linux_Ubuntu${UBUNTU_RELEASE_YEAR}.run ; ./ZED_SDK_Linux_Ubuntu${UBUNTU_RELEASE_YEAR}.run silent skip_cuda && \
    ln -sf /lib/x86_64-linux-gnu/libusb-1.0.so.0 /usr/lib/x86_64-linux-gnu/libusb-1.0.so && \
    rm ZED_SDK_Linux_Ubuntu${UBUNTU_RELEASE_YEAR}.run && \
    rm -rf /var/lib/apt/lists/*

# Make some tools happy
RUN mkdir -p /root/Documents/ZED/

# Create a user named "docker" without a password
RUN useradd -m docker
# Allow the "docker" user to use sudo without a password
RUN echo 'docker ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

USER docker
CMD ["/bin/bash"]
WORKDIR /scintilla
