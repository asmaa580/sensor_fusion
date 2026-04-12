import rclpy
from rclpy.node import Node

from nav_msgs.msg import Odometry
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Quaternion
import math
import random

def create_quaternion(yaw):
    # Convert yaw (in radians) to quaternion
    return Quaternion(
        x=0.0,
        y=0.0,
        z=math.sin(yaw / 2.0),
        w=math.cos(yaw / 2.0)
    )

class FakeSensorPublisher(Node):
    def __init__(self):
        super().__init__('fake_sensor_publisher')

        # Publishers
        self.odom_pub = self.create_publisher(Odometry, '/camera/odom', 10)
        self.gps_pub = self.create_publisher(Odometry, '/odometry/gps', 10)
        self.imu_pub = self.create_publisher(Imu, '/imu/data', 10)

        # Timers
        self.create_timer(0.1, self.publish_camera_odom)  # 10 Hz
        self.create_timer(1.0, self.publish_gps)          # 1 Hz
        self.create_timer(0.05, self.publish_imu)         # 20 Hz

        self.x = 0.0
        self.y = 0.0
        self.yaw = 0.0

    def publish_camera_odom(self):
        msg = Odometry()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'odom'
        msg.child_frame_id = 'base_link'

        # Simulate forward motion
        self.x += 0.05
        self.yaw += 0.01

        msg.pose.pose.position.x = self.x
        msg.pose.pose.position.y = self.y
        msg.pose.pose.orientation = create_quaternion(self.yaw)

        msg.twist.twist.linear.x = 0.5
        msg.twist.twist.angular.z = 0.1

        self.odom_pub.publish(msg)

    def publish_gps(self):
        msg = Odometry()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'map'
        msg.child_frame_id = 'base_link'

        # GPS is noisy
        msg.pose.pose.position.x = self.x + random.uniform(-0.2, 0.2)
        msg.pose.pose.position.y = self.y + random.uniform(-0.2, 0.2)

        self.gps_pub.publish(msg)

    def publish_imu(self):
        msg = Imu()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'base_link'

        msg.orientation = create_quaternion(self.yaw)
        msg.angular_velocity.z = 0.1
        msg.linear_acceleration.x = 0.0
        msg.linear_acceleration.y = 0.0
        msg.linear_acceleration.z = 0.0

        self.imu_pub.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = FakeSensorPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
