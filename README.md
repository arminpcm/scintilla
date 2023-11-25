# scintilla
The road to a better world for visually impaired

## How to setup the repo
Start with setting up your host compuer. Currently, we are supporting Ubuntu 22.04 host and Ubuntu 20.04 on the AGX board.

### Prepare host
```
cd scripts
sudo ./container/dev_setup.sh
source ~/.bashrc
```

To ensure emulation is working, try the following command:
```
docker run --rm --platform=linux/arm64 -t arm64v8/ubuntu uname -m
```

This should print `aarch64` on the terminal.

For ease of use, you can source `scriots/aliases.sh` in your bashrc file:
```
source $SCINTILLA_ROOT/scripts/aliases.sh
```

### Build docker image

```
./container/build.sh <platform>
# Platform can be either arm or x86
# Or use `build` or `builda` that is set using aliases
```

Note: Currently, L4T docker is supported through QEMU. Also x86 docker image is based on Cuda12 and Ubuntu 22.04.

Settings for the docker build process (OS version, Cuda version, etc.) are maintained in [settings.sh](container/settings.sh) file.

### Using the docker images
You will have multiple scripts at your disposal to start, stop, and dive into an already started docker container:

```
# To start a docker image (arm or x86)
./container/start <platform>
# To go inside a docker running docker container (arm or x86)
./container/into <platform>
# To stop a docker image (arm or x86)
./container/stop <platform>
```

### Building ROS2 package for Stereo Zed

```
sudo chown -R docker /thirdparty/*
cd /thirdparty/ros2_ws
source /opt/ros/foxy/setup.bash
sudo rosdep init
rosdep update
rosdep install --from-paths src --ignore-src --rosdistro foxy -r -y
colcon build --symlink-install --cmake-args=-DCMAKE_BUILD_TYPE=Release
echo "source /thirdparty/zed-ros2-wrapper/install/local_setup.bash" >> ~/.bashrc
source ~/.bashrc
```