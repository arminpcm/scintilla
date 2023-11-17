# scintilla
The road to a better world for visually impaired

## How to setup the repo
Start with setting up your host compuer. Currently, we are supporting Ubuntu 22.04 host and Ubuntu 20.04 on the AGX board.

### Prepare host
```
cd scripts
sudo ./dev_setup.sh
```

To ensure emulation is working, try the following command:
```
docker run --rm --platform=linux/arm64 -t arm64v8/ubuntu uname -m
```

This should print `aarch64` on the terminal.

### Build docker image

```
cd container
./build.sh
```
