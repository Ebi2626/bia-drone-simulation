#!/bin/bash
# run.sh - Skrypt uruchamiania kontenera ROS2 z Gazebo Classic

# Dostęp do X11 dla lokalnych połączeń
xhost +local:

# Nazwa obrazu i kontenera
IMAGE_NAME="ros2_px4_swarm:latest"
CONTAINER_NAME="ros2_px4_dev"

echo "Uruchamianie kontenera $CONTAINER_NAME..."

# Uruchomienie kontenera z odpowiednimi opcjami
podman run -it --rm --replace \
  --net=host \
  --ipc=host \
  --pid=host \
  --security-opt label=disable \
  --userns=keep-id \
  --env DISPLAY=$DISPLAY \
  --env QT_X11_NO_MITSHM=1 \
  --env NVIDIA_DRIVER_CAPABILITIES=all \
  --env NVIDIA_VISIBLE_DEVICES=all \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  -v ~/simulation/ros2/src:/home/ros2user/ros2_ws/src/my_swarm_planning:rw \
  --device=nvidia.com/gpu=all \
  --workdir /home/ros2user/ros2_ws/src/my_swarm_planning \
  --name $CONTAINER_NAME \
  $IMAGE_NAME

# Cofanie dostępu do X11 dla lokalnych połączeń ze względów bezpieczeństwa
xhost -local:
