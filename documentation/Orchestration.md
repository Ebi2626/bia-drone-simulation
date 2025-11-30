# Orchestration
To ensure the entire PX4 SITL + MicroXRCEAgent + ROS2 stack works correctly, **the startup order is important** for proper network initialization and time synchronization.

## Recommended Startup Sequence

1. **Start MicroXRCEAgent first**

   - This agent acts as the intermediary broker for DDS messages between PX4 SITL and ROS2.
   - It must be ready and listening on the specified UDP port before PX4 tries to connect.
   - If PX4 starts first, it will repeatedly fail to synchronize time and establish the DDS session.

   Example command inside the container or host:

`MicroXRCEAgent udp4 -p 8888 &`


The agent runs in the background and listens on port 8888.

2. **Start PX4 SITL instance**

- Once the agent is running and reachable, PX4 SITL can be started.
- PX4 will connect to the agent's UDP port for DDS communication.
- PX4 initializes its simulation loop and starts sending/receiving messages through MicroXRCEAgent.

Example command:

`
export PX4_SIM_MODEL=gz_x500
export PX4_SYS_AUTOSTART=4001
./build/px4_sitl_default/bin/px4 -i 0 -p 8888
`


3. **Start your ROS2 nodes (optional but typical in swarm research)**

- After PX4 SITL and MicroXRCEAgent are running and connected, start your ROS2 offboard control nodes.
- These nodes communicate with PX4 through MicroXRCEAgent using ROS2 topics.

Example:

`
source /opt/ros/humble/setup.bash
source /opt/ros2_ws/install/setup.bash
ros2 run your_package your_node
`


## Why this order?

- PX4 SITL depends on MicroXRCEAgent being active to establish DDS communication.
- Time synchronization between PX4 and the agent is automatic after the agent is reachable.
- Starting PX4 without an active agent causes repeated connection timeouts and failed synchronization logs.
- ROS2 offboard control nodes rely on PX4 and MicroXRCEAgent to be ready.

## Summary

| Step | Component           | Purpose                                   |
|-------|---------------------|-------------------------------------------|
| 1     | MicroXRCEAgent      | Broker DDS messages & enable communication |
| 2     | PX4 SITL            | Run autopilot and simulation logic         |
| 3     | ROS2 Offboard Nodes | Execute control/planning algorithms        |

Following this startup sequence ensures a stable and functional simulation environment suited for scalable multi-drone swarm research using PX4, MicroXRCEAgent, and ROS2.
