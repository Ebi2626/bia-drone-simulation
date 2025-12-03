#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy, DurabilityPolicy
from px4_msgs.msg import OffboardControlMode, TrajectorySetpoint, VehicleCommand, VehicleOdometry
import math

class OffboardMission(Node):
    def __init__(self):
        super().__init__('offboard_mission_control')

        # =======================================================================
        # 1. DEFINICJA PUNKTÓW MISJI (Wektory X, Y, Z)
        # Uwaga: Układ współrzędnych NED (North-East-Down).
        # X+ = Północ, Y+ = Wschód, Z- = Góra (dlatego wysokość jest ujemna!)
        # =======================================================================
        
        # Punkt startowy (np. wzniesienie się nad miejsce spawnu)
        # [X, Y, Z]
        self.start_point = [2662.302490, -2583.753174, -40.242710] 

        # Punkt docelowy (gdzie dron ma polecieć)
        # [X, Y, Z]
        self.goal_point = [-2622.284668, 2343.222168, -43.132080]

        # Tolerancja dotarcia do punktu (w metrach)
        self.acceptance_radius = 0.5

        # =======================================================================

        # Konfiguracja QoS - niezbędna do komunikacji z PX4
        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            durability=DurabilityPolicy.TRANSIENT_LOCAL,
            history=HistoryPolicy.KEEP_LAST,
            depth=1
        )

        # Publishery
        self.offboard_mode_pub = self.create_publisher(
            OffboardControlMode, '/fmu/in/offboard_control_mode', qos_profile)
        self.trajectory_pub = self.create_publisher(
            TrajectorySetpoint, '/fmu/in/trajectory_setpoint', qos_profile)
        self.command_pub = self.create_publisher(
            VehicleCommand, '/fmu/in/vehicle_command', qos_profile)
        
        # Subscriber - musimy wiedzieć gdzie jest dron!
        self.odom_sub = self.create_subscription(
            VehicleOdometry, '/fmu/out/vehicle_odometry', self.odom_callback, qos_profile)

        # Zmienne wewnętrzne
        self.timer = self.create_timer(0.1, self.timer_callback) # 10Hz
        self.counter = 0
        self.current_position = [0.0, 0.0, 0.0]
        self.mission_state = "INIT" # INIT, CLIMB, FLY_TO_GOAL, LAND, FINISHED

        self.get_logger().info("Mission Node Initialized. Waiting for offboard...")

    def odom_callback(self, msg):
        # Aktualizacja pozycji drona z odometrii
        self.current_position = msg.position

    def timer_callback(self):
        # 1. ZAWSZE publikuj Heartbeat trybu Offboard (wymagane przez PX4)
        self.publish_offboard_control_mode()

        # 2. Logika misji (Maszyna Stanów)
        if self.mission_state == "INIT":
            # Wymagane "rozgrzanie" strumienia setpointów przed przełączeniem trybu
            self.publish_trajectory_setpoint(self.start_point) # Wysyłamy 0,0,-5
            
            if self.counter == 10:
                self.engage_offboard_mode()
                self.arm()
                self.mission_state = "CLIMB"
                self.get_logger().info(f"Taking off to Start Point: {self.start_point}")

        elif self.mission_state == "CLIMB":
            # Faza 1: Lot do punktu startowego (wznoszenie)
            self.publish_trajectory_setpoint(self.start_point)
            
            dist = self.calculate_distance(self.current_position, self.start_point)
            if dist < self.acceptance_radius:
                self.mission_state = "FLY_TO_GOAL"
                self.get_logger().info(f"Start Point Reached. Flying to Goal: {self.goal_point}")

        elif self.mission_state == "FLY_TO_GOAL":
            # Faza 2: Przelot do punktu docelowego
            self.publish_trajectory_setpoint(self.goal_point)
            
            dist = self.calculate_distance(self.current_position, self.goal_point)
            if dist < self.acceptance_radius:
                self.mission_state = "LAND"
                self.get_logger().info("Goal Reached. Landing...")

        elif self.mission_state == "LAND":
            # Faza 3: Lądowanie
            # W tej fazie przestajemy wysyłać setpointy pozycyjne, 
            # wysyłamy komendę lądowania raz, a potem monitorujemy status
            self.land()
            self.mission_state = "FINISHED"

        elif self.mission_state == "FINISHED":
            # Misja zakończona, nic nie rób (heartbeat nadal leci)
            pass

        self.counter += 1

    # --- Funkcje pomocnicze ---

    def calculate_distance(self, pos1, pos2):
        return math.sqrt(
            (pos1[0] - pos2[0])**2 + 
            (pos1[1] - pos2[1])**2 + 
            (pos1[2] - pos2[2])**2
        )

    def publish_offboard_control_mode(self):
        msg = OffboardControlMode()
        msg.position = True
        msg.velocity = False
        msg.acceleration = False
        msg.timestamp = int(self.get_clock().now().nanoseconds / 1000)
        self.offboard_mode_pub.publish(msg)

    def publish_trajectory_setpoint(self, point_vector):
        msg = TrajectorySetpoint()
        msg.position = point_vector # [X, Y, Z]
        msg.yaw = 0.0 # Stały kąt (Północ)
        msg.timestamp = int(self.get_clock().now().nanoseconds / 1000)
        self.trajectory_pub.publish(msg)

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

    def engage_offboard_mode(self):
        self.publish_vehicle_command(VehicleCommand.VEHICLE_CMD_DO_SET_MODE, 1.0, 6.0)

    def arm(self):
        self.publish_vehicle_command(VehicleCommand.VEHICLE_CMD_COMPONENT_ARM_DISARM, 1.0)

    def land(self):
        self.publish_vehicle_command(VehicleCommand.VEHICLE_CMD_NAV_LAND)


def main():
    rclpy.init()
    node = OffboardMission()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
