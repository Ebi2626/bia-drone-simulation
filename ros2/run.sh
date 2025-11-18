#!/bin/bash
# run.sh - Skrypt uruchamiania kontenera ROS2 z GUI

# Włącz dostęp do X11
xhost +local:

# Uruchom kontener z obsługą GUI
podman run -it --rm \
  --net=host \
  --ipc=host \
  -e DISPLAY=$DISPLAY \
  -e QT_X11_NO_MITSHM=1 \
  -v /tmp/.X11-unix:/tmp/.X11-unix:Z \
  -v ~/simulation/ros2/src:/ros2_ws/src:Z \
  --device=/dev/dri \
  --name ros2_gui \
  ros2-jazzy-gui

# Po wyjściu z kontenera, przywróć zabezpieczenia X11
xhost -local:
