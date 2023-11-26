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

For ease of use, you can source `scripts/aliases.sh` in your bashrc file:
```
source $SCINTILLA_ROOT/scripts/aliases.sh
source ~/.bashrc
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
./scripts/build_zed_wrapper.sh
source ~/.bashrc
```

Now launch the ros2 nodes:
```
ros2 launch zed_wrapper zed_camera.launch.py camera_model:=zed2i
```

# Things I need to do:
1. Add modules to python path:
```
export PYTHONPATH=$PYTHONPATH:$SCINTILLA_ROOT/modules
```
2. Add SCINTILLA_ROOT to the docker
3. Make sure logs are captured in the right place
