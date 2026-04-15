import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Imu, NavSatFix
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Quaternion
from std_msgs.msg import Header

import math

def yaw_to_quaternion(yaw: float) -> Quaternion:
    """Convert yaw (in radians) to a quaternion."""
    q = Quaternion()
    q.z = math.sin(yaw / 2.0)
    q.w = math.cos(yaw / 2.0)
    return q

class FakeSensors(Node):

    def __init__(self):
        super().__init__('fake_sensors')

        # Publishers
        self.imu_pub = self.create_publisher(Imu, '/imu/data', 10)
        self.odom_pub = self.create_publisher(Odometry, '/camera/odom', 10)
        self.gps_pub = self.create_publisher(NavSatFix, '/gps/fix', 10)

        # Simulation time
        self.t = 0.0
        self.timer = self.create_timer(0.1, self.publish_data)

    def publish_data(self):
        self.t += 0.1

        # Fake motion: straight line forward
        x = self.t
        y = 0.0
        yaw = 0.0

        # ======================
        # ODOMETRY
        # ======================
        odom = Odometry()
        odom.header = Header()
        odom.header.stamp = self.get_clock().now().to_msg()
        odom.header.frame_id = "odom"
        odom.child_frame_id = "base_link"

        odom.pose.pose.position.x = x
        odom.pose.pose.position.y = y
        odom.pose.pose.orientation = yaw_to_quaternion(yaw)

        odom.twist.twist.linear.x = 1.0

        # Covariance (nonzero so EKF trusts it)
        odom.pose.covariance = [
            0.05, 0, 0, 0, 0, 0,
            0, 0.05, 0, 0, 0, 0,
            0, 0, 0.1, 0, 0, 0,
            0, 0, 0, 0.1, 0, 0,
            0, 0, 0, 0, 0.1, 0,
            0, 0, 0, 0, 0, 0.1
        ]

        self.odom_pub.publish(odom)

        # ======================
        # IMU
        # ======================
        imu = Imu()
        imu.header = Header()
        imu.header.stamp = self.get_clock().now().to_msg()
        imu.header.frame_id = "base_link"

        imu.orientation = yaw_to_quaternion(yaw)
        imu.angular_velocity.z = 0.0
        imu.linear_acceleration.x = 0.0
        imu.linear_acceleration.y = 0.0
        imu.linear_acceleration.z = 0.0

        # Covariances (realistic small values)
        imu.orientation_covariance = [0.01, 0, 0,
                                      0, 0.01, 0,
                                      0, 0, 0.01]
        imu.angular_velocity_covariance = [0.001, 0, 0,
                                           0, 0.001, 0,
                                           0, 0, 0.001]
        imu.linear_acceleration_covariance = [0.1, 0, 0,
                                              0, 0.1, 0,
                                              0, 0, 0.1]

        self.imu_pub.publish(imu)

        # ======================
        # GPS
        # ======================
        gps = NavSatFix()
        gps.header = Header()
        gps.header.stamp = self.get_clock().now().to_msg()
        gps.header.frame_id = "gps_link"

        gps.latitude = 30.0 + x * 0.00001
        gps.longitude = 31.0 + y * 0.00001
        gps.altitude = 0.0

        # Covariance (approximate GPS accuracy ~3m)
        gps.position_covariance = [9.0, 0, 0,
                                   0, 9.0, 0,
                                   0, 0, 16.0]
        gps.position_covariance_type = NavSatFix.COVARIANCE_TYPE_APPROXIMATED

        self.gps_pub.publish(gps)


def main(args=None):
    rclpy.init(args=args)
    node = FakeSensors()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
