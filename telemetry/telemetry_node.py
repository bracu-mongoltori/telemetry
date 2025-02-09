import serial
from time import sleep
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class TelemetryAutonomous(Node):
    def __init__(self, port="/dev/ttyUSB0", baudrate=57600, mode = "base"):
        super().__init__('telemetry_node')
        self.ser = serial.Serial(port, baudrate)
        self.cmd_vel_topic = "cmd_vel_telemetry"
        self.cmd_vel_telemetry = self.create_subscription(Twist, self.cmd_vel_topic, self.cmd_vel_callback, 10)
        self.cmd_vel_irl = self.create_publisher(Twist, "cmd_vel", 10)
        self.get_logger().info("Telemetry Node Started")
        self.parsed_twist_msg = Twist()
        self.irl_msg_publisher = self.create_timer(0.1, self.real_msg_publisher)
        self.mode = mode


    def read(self):
        data = self.ser.readline().decode("utf-8")
        parsed_data = data.split()
        if parsed_data[0] == self.cmd_vel_topic:
            self.parsed_twist_msg = Twist()
            self.parsed_twist_msg.linear.x = float(parsed_data[2])
            self.parsed_twist_msg.angular.z = float(parsed_data[4])

    def write(self, data):
        self.ser.write(bytes(data + "\n", 'utf-8'))

    def real_msg_publisher(self):
        if self.mode == "rover":
            self.get_logger().info(f"Publishing {self.parsed_twist_msg}")
            self.cmd_vel_irl.publish(self.parsed_twist_msg)

    def cmd_vel_callback(self, msg):
        x = msg.linear.x
        z = msg.angular.z
        self.write(f"cmd_vel lin_x {x} ang_z {z}")
    
def main(args=None):
    rclpy.init(args=args)
    t = TelemetryAutonomous()
    rclpy.spin(t)
    rclpy.shutdown()

# def main(args=None): #for rover
#     rclpy.init(args=args)
#     t = TelemetryAutonomous(mode="rover")
#     rclpy.spin(t)
#     rclpy.shutdown()

if __name__ == "__main__":
    t = TelemetryAutonomous()
    while True:
        inp = input("> Enter data: ")
        t.write(inp)
        sleep(.1)
        # print(t.read())
        # sleep(1)