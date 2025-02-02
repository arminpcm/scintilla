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

FROM nvidia/cuda:${CUDA_MAJOR}.${CUDA_MINOR}-devel-ubuntu${UBUNTU_RELEASE_YEAR}.04

ARG UBUNTU_RELEASE_YEAR
ARG CUDA_MAJOR
ARG CUDA_MINOR
ARG ZED_SDK_MAJOR
ARG ZED_SDK_MINOR

SHELL ["/bin/bash", "-c"]

ENV NVIDIA_DRIVER_CAPABILITIES \
    ${NVIDIA_DRIVER_CAPABILITIES:+$NVIDIA_DRIVER_CAPABILITIES,}compute,video,utility

RUN echo "America/Toronto" > /etc/localtime && echo "CUDA Version ${CUDA_MAJOR}.${CUDA_MINOR}" > /usr/local/cuda/version.txt
RUN export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/usr/local/cuda/lib64/"

# Setup the ZED SDK
RUN apt update -y || true && apt install --no-install-recommends lsb-release wget less udev sudo zstd build-essential cmake python3 python3-pip libpng-dev libgomp1 -y && \
    python3 -m pip install numpy opencv-python && \
    wget -q -O ZED_SDK_Linux_Ubuntu${UBUNTU_RELEASE_YEAR}.run https://download.stereolabs.com/zedsdk/${ZED_SDK_MAJOR}.${ZED_SDK_MINOR}/cu${CUDA_MAJOR}${CUDA_MINOR%.*}/ubuntu${UBUNTU_RELEASE_YEAR} && \
    chmod +x ZED_SDK_Linux_Ubuntu${UBUNTU_RELEASE_YEAR}.run && ./ZED_SDK_Linux_Ubuntu${UBUNTU_RELEASE_YEAR}.run -- silent skip_tools skip_cuda && \
    ln -sf /lib/x86_64-linux-gnu/libusb-1.0.so.0 /usr/lib/x86_64-linux-gnu/libusb-1.0.so && \
    rm ZED_SDK_Linux_Ubuntu${UBUNTU_RELEASE_YEAR}.run && \
    rm -rf /var/lib/apt/lists/*

# Install ROS2
RUN apt update -y && apt install -y locales locales-all && \
    locale-gen en_US en_US.UTF-8 && \
    update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8 && \
    export LANG=en_US.UTF-8 && \
    apt install -y software-properties-common && \
    export DEBIAN_FRONTEND=noninteractive && \
    add-apt-repository universe && \
    apt update -y && apt install -y curl && \
    curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | tee /etc/apt/sources.list.d/ros2.list > /dev/null && \
    apt update -y && apt install -y ros-dev-tools && \
    apt update -y && apt upgrade -y && apt install -y ros-iron-desktop && \
    source /opt/ros/iron/setup.bash && \
    rm -rf /var/lib/apt/lists/*

# Add ZED ROS2 wrapper to the docker
COPY thirdparty/zed-ros2-wrapper.zip /thirdparty/zed-ros2-wrapper.zip
RUN apt update -y && apt install -y unzip && \
    cd /thirdparty && \
    mkdir -p ros2_ws/src/ && \
    unzip zed-ros2-wrapper.zip -d ros2_ws/src/zed-ros2-wrapper && \
    rm zed-ros2-wrapper.zip

# Install development tools
RUN pip3 install dash \
                 plotly \
                 pandas \
                 pyarrow \
                 dash-bootstrap-components \
                 mcap \
                 open3d

# Create a user named "docker" without a password
RUN useradd -m docker
# Allow the "docker" user to use sudo without a password
RUN echo 'docker ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

COPY scripts/.prompt.sh /home/.prompt.sh
COPY container/entrypoint.sh /home/entrypoint.sh

RUN usermod -a -G video docker
USER docker

CMD ["/bin/bash"]
WORKDIR /scintilla
