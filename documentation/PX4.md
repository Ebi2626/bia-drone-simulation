# PX4
The `px4` executable is the core binary of the PX4 autopilot software used for Software-In-The-Loop (SITL) simulations. It runs the flight control algorithms, communicates with the simulator (e.g., Gazebo), and handles interactions via middleware like Micro XRCE DDS.

## Purpose of the `px4` Command

- Launches the full PX4 flight stack for simulation or real hardware.
- Interfaces with simulators (Gazebo, AirSim, etc.) and communication middleware.
- Manages multiple drone instances for swarm simulations using instance-specific parameters.

## Key Flags and Environment Variables for `px4`

| Flag/Variable                | Description                                                                                              | Usage in Drone Swarm Simulations                                                                                           |
|-----------------------------|----------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------|
| `-i <instance_id>`            | Specifies the instance index of the PX4 node. Essential when running multiple drones to avoid conflicts. | Each drone in a swarm gets a unique `-i` value (e.g., 0, 1, 2, ...) to differentiate communication, control, and logging.    |
| `PX4_SIM_MODEL=<model>`       | Sets the specific drone model for simulation (e.g., `gz_x500`, `none_iris`). Determines vehicle and environment. | Allows running different types of vehicles simultaneously in swarm simulations by changing this variable per instance.      |
| `PX4_SYS_AUTOSTART=<autostart>` | Specifies a preconfigured system autostart ID. It defines default parameters and sensor configurations.       | Use to quickly load the correct configuration for the drone model/environment without manual parameter setting.             |
| `-p <agent_port>`             | Sets the UDP port MicroXRCEAgent uses for communication with this PX4 instance.                            | Critical in swarms where each drone's PX4 instance communicates through a unique port so that agents and PX4 clients pair correctly. |
| `--verbose`                  | Enables verbose logging for debugging purposes.                                                         | Useful during development of algorithms or debugging inter-drone communication in swarm setups.                             |
| `--no-mavlink`               | Disables MAVLink communication.                                                                          | Can reduce overhead if ROS2/RTPS based communication is fully used in swarm configurations.                                  |

## Typical Usage Example for a Single Drone

`
export PX4_SIM_MODEL=gz_x500
export PX4_SYS_AUTOSTART=4001
./build/px4_sitl_default/bin/px4 -i 0
`


- This runs one drone simulation instance with model `gz_x500` and autostart config `4001`.

## Running Multiple PX4 SITL Instances for a Swarm

For a swarm of N drones, launch N PX4 instances with unique instance IDs and communication ports:

### Drone 1
` 
export PX4_SIM_MODEL=gz_x500
export PX4_SYS_AUTOSTART=4001
./build/px4_sitl_default/bin/px4 -i 0 -p 8888 &`

### Drone 2
`
export PX4_SIM_MODEL=gz_x500
export PX4_SYS_AUTOSTART=4001
./build/px4_sitl_default/bin/px4 -i 1 -p 8889 &
`

### Drone 3
`
export PX4_SIM_MODEL=gz_x500
export PX4_SYS_AUTOSTART=4001
./build/px4_sitl_default/bin/px4 -i 2 -p 8890 &`


- Each instance should correspond with a MicroXRCEAgent listening on the same port specified by `-p`.
- Unique `-i` ensures data separation and conflict-free control channels.
- Different `PX4_SIM_MODEL` values can enable heterogeneous swarms.

## Important Notes

- The `-p` port option is essential for DDS (MicroXRCE) communication; no two agents/drone instances should share the same port.
- `PX4_SYS_AUTOSTART` loads predefined parameters; ensure you use the correct number for your vehicle and simulation environment.
- Avoid running multiple instances with the same `-i` or port to prevent communication conflicts.

## Summary

The `px4` command with its instance `-i` flag and environment variables like `PX4_SIM_MODEL` and `PX4_SYS_AUTOSTART` forms the basis for controlling multiple drones in simulation. Combined with MicroXRCEAgent instances listening on unique UDP ports, it supports scalable and modular swarm simulations.

Successfully mastering these options enables robust research on bio-inspired swarm path planning algorithms using PX4 SITL and ROS2 [web:19][web:134][web:118].



