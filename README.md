# bia-drone-simulation

This repository contains an experiment on the efficiency of bio-inspired algorithms in path planning for drone swarms. The objective of this project is to compare the Osprey Optimization Algorithm, Multiple Swarm Fruit Fly Optimization Algorithm**,** and Sparrow Search Algorithm for path planning of drone swarms in a dynamic environment (with obstacles).

## Technologies
The main target of this simulation is to provide the closest-to-real-life environment to verify the listed algorithms**'** efficiency in the most realistic way. To achieve that**,** I decided to use the following stack:

- Podman - for portability (and to support open source!)

- Bash - for OS scripting

- ROS2 - for controlling drones

- PX4 - for drone autopilot

- Gazebo - for visualization

- Python - for architecture, algorithms**,** and main logic

- Ubuntu - for launching the rest of the tools

- Git - to manage this repository

- YAML - for config files

## Scenarios

The main purpose of this project is to test path planning for drone swarms with 3 different algorithms. To avoid false results**,** there are 3 different environments with different amounts and configurations of obstacles:

- Plain space

- Suburban area (few obstacles)

- Urban area (many obstacles)

To make the results more objective, results achieved by those algorithms will be compared to the results of NSGA-III as one of the most researched algorithms in that area.

## Scenarios

Main purpose of this project is to test path planning for drone swarms with 3 differenet algorithms. To avoid false results there are 3 differenet environments with different amount and configuration of obstacles. 
    1. Plain space
    2. Suburban area (few obstacles)
    3. Urban area (many obstacles)

To make results a little bit more objective results achived by those algorithms will be compared to the result of NSGA-III as one of the most researched algorithms in that area.

## Project structure


    |__ README.md - project documentation
    |
    |── ros2 - folder with ROS2 files
        |
        ├── build.sh - building podman image
        |
        ├── Dockerfile - podman image
        |
        ├── run.sh - running podman container
        |
        └── src - simulation source files





