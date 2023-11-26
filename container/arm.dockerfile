################################################################################
# Dockerfile for Scintilla
# Copyright (c) 2023 Scintilla. All rights reserved.
#
# This Dockerfile is private and confidential. Unauthorized copying or
# reproduction of this file, via any medium, is strictly prohibited without
# the explicit permission of Scintilla.
#
################################################################################

# Base docker: https://ngc.nvidia.com/catalog/containers/nvidia:l4t-base

ARG L4T_MAJOR_VERSION
ARG L4T_MINOR_VERSION
ARG L4T_PATCH_VERSION
ARG L4T_BASE_IMAGE

FROM nvcr.io/nvidia/${L4T_BASE_IMAGE}:r${L4T_MAJOR_VERSION}.${L4T_MINOR_VERSION}.${L4T_PATCH_VERSION}

ARG L4T_MAJOR_VERSION
ARG L4T_MINOR_VERSION
ARG L4T_PATCH_VERSION
ARG ZED_SDK_MAJOR
ARG ZED_SDK_MINOR

#This environment variable is needed to use the streaming features on Jetson inside a container
ENV LOGNAME root
ENV DEBIAN_FRONTEND noninteractive
SHELL ["/bin/bash", "-c"]
RUN apt update -y || true ; apt install --no-install-recommends lsb-release wget less zstd udev sudo apt-transport-https -y && \
    echo "# R${L4T_MAJOR_VERSION} (release), REVISION: ${L4T_MINOR_VERSION}.${L4T_PATCH_VERSION}" > /etc/nv_tegra_release ; \
    wget -q --no-check-certificate -O ZED_SDK_Linux.run https://download.stereolabs.com/zedsdk/${ZED_SDK_MAJOR}.${ZED_SDK_MINOR}/l4t${L4T_MAJOR_VERSION}.${L4T_MINOR_VERSION}/jetsons && \
    chmod +x ZED_SDK_Linux.run ; ./ZED_SDK_Linux.run silent skip_tools skip_drivers && \
    rm -rf /usr/local/zed/resources/* \
    rm -rf ZED_SDK_Linux.run && \
    rm -rf /var/lib/apt/lists/*

# ZED Python API
RUN apt update -y || true ; apt install --no-install-recommends python3 python3-pip python3-dev python3-setuptools build-essential -y && \ 
    wget download.stereolabs.com/zedsdk/pyzed -O /usr/local/zed/get_python_api.py && \
    python3 /usr/local/zed/get_python_api.py && \
    python3 -m pip install cython wheel && \
    python3 -m pip install numpy pyopengl *.whl && \
    apt remove --purge build-essential -y && apt autoremove -y && \
    rm *.whl ; rm -rf /var/lib/apt/lists/*

#This symbolic link is needed to use the streaming features on Jetson inside a container
RUN ln -sf /usr/lib/aarch64-linux-gnu/tegra/libv4l2.so.0 /usr/lib/aarch64-linux-gnu/libv4l2.so

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
