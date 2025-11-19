#!/bin/bash
# build.sh - Skrypt budowania obrazu ROS2

podman build --ipc=private --pid=private --network=slirp4netns:allow_host_loopback=true --memory=16g --ulimit nofile=65536:65536 -t ros2_px4_swarm:latest .
