#!/bin/bash
# build.sh - Skrypt budowania obrazu ROS2

podman build \
    --format docker \
    --ipc=host \
    --pid=private \
    --network=host \
    --memory=16g \
    --ulimit nofile=65536:65536 \
    -t ros2_px4_swarm:latest .
