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
$SCINTILLA_ROOT/container/build.sh <platform>
# Platform can be either arm or x86
# Or use `build` or `builda` that is set using aliases
```

Note: Currently, L4T docker is supported through QEMU. Also x86 docker image is based on Cuda12 and Ubuntu 22.04.

Settings for the docker build process (OS version, Cuda version, etc.) are maintained in [settings.sh](container/settings.sh) file.

### Using the docker images
You will have multiple scripts at your disposal to start, stop, and dive into an already started docker container:

```
# To start a docker image (arm or x86)
$SCINTILLA_ROOT/container/start <platform>
# To go inside a docker running docker container (arm or x86)
$SCINTILLA_ROOT/container/into <platform>
# To stop a docker image (arm or x86)
$SCINTILLA_ROOT/container/stop <platform>
```

Starting the database containers
```
docker-compose up -d
```

### Building ROS2 package for Stereo Zed

```
$SCINTILLA_ROOT/scripts/build_zed_wrapper.sh
source ~/.bashrc
```

Now launch the ros2 nodes:
```
source /opt/ros/iron/setup.bash
ros2 launch zed_wrapper zed_camera.launch.py camera_model:=zed2i
```


### Using the data pipeline

## Data Extraction
```
python3 modules/data_pipeline/extractors/mcap_to_parquet.py data/logs/collected/robot_log_20231126_204614/robot_log_20231126_204614.mcap 
```

## Working with data pipeline
Starting airflow
```
airflow standalone
# Visit localhost:8080
```
