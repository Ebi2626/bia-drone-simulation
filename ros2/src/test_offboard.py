#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from px4_msgs.msg import OffboardControlMode, TrajectorySetpoint, VehicleCommand

class OffboardControl(Node):
    def __init__(self):
        super().__init__('offboard_control')
        
        # Publishery - wysyłają komendy do PX4
        self.offboard_mode_pub = self.create_publisher(
            OffboardControlMode, '/fmu/in/offboard_control_mode', 10)
        self.trajectory_pub = self.create_publisher(
            TrajectorySetpoint, '/fmu/in/trajectory_setpoint', 10)
        self.command_pub = self.create_publisher(
            VehicleCommand, '/fmu/in/vehicle_command', 10)
        
        # Timer - co 100ms wysyła komendy
        self.timer = self.create_timer(0.1, self.timer_callback)
        self.counter = 0
    
    def timer_callback(self):
        # 1. Wyślij OffboardControlMode (60Hz minimum!)
        offboard_msg = OffboardControlMode()
        offboard_msg.position = True  # Kontrola pozycji
        offboard_msg.velocity = False
        offboard_msg.acceleration = False
        offboard_msg.timestamp = int(self.get_clock().now().nanoseconds / 1000)
        self.offboard_mode_pub.publish(offboard_msg)
        
        # 2. Wyślij TrajectorySetpoint (trajektoria z algorytmu)
        trajectory_msg = TrajectorySetpoint()
        trajectory_msg.position = [0.0, 0.0, -5.0]  # X, Y, Z (Z ujemne = w górę!)
        trajectory_msg.yaw = 0.0
        trajectory_msg.timestamp = int(self.get_clock().now().nanoseconds / 1000)
        self.trajectory_pub.publish(trajectory_msg)
        
        # 3. Po 10 cyklach: przełącz na offboard i arm
        if self.counter == 10:
            self.publish_vehicle_command(VehicleCommand.VEHICLE_CMD_DO_SET_MODE, 1.0, 6.0)
            self.publish_vehicle_command(VehicleCommand.VEHICLE_CMD_COMPONENT_ARM_DISARM, 1.0)
        
        self.counter += 1
    
    def publish_vehicle_command(self, command, param1=0.0, param2=0.0):
        msg = VehicleCommand()
        msg.command = command
        msg.param1 = param1
        msg.param2 = param2
        msg.target_system = 1
        msg.target_component = 1
        msg.source_system = 1
        msg.source_component = 1
        msg.from_external = True
        msg.timestamp = int(self.get_clock().now().nanoseconds / 1000)
        self.command_pub.publish(msg)

def main():
    rclpy.init()
    node = OffboardControl()
    rclpy.spin(node)

if __name__ == '__main__':
    main()
