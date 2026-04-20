import rclpy
from rclpy.node import Node

from geometry_msgs.msg import PointStamped
from sensor_msgs.msg import NavSatFix, NavSatStatus


class GPSConverter(Node):

    def __init__(self):
        super().__init__('gps_point_to_navsat')

        # Subscriber (your Webots GPS)
        self.subscription = self.create_subscription(
            PointStamped,
            '/TurtleBot3Burger/gps',
            self.gps_callback,
            10
        )

        # Publisher (NavSatFix for EKF)
        self.publisher = self.create_publisher(
            NavSatFix,
            '/gps/fix',
            10
        )

        self.get_logger().info("GPS Point → NavSatFix converter started")

    def gps_callback(self, msg: PointStamped):

        navsat = NavSatFix()

        # FIXED TIMESTAMP (VERY IMPORTANT)
        navsat.header.stamp = msg.header.stamp
        navsat.header.frame_id = "gps"

        navsat.latitude = float(msg.point.x)
        navsat.longitude = float(msg.point.y)
        navsat.altitude = float(msg.point.z)

        navsat.status = NavSatStatus()
        navsat.status.status = NavSatStatus.STATUS_FIX
        navsat.status.service = NavSatStatus.SERVICE_GPS

        navsat.position_covariance = [
            1.0, 0.0, 0.0,
            0.0, 1.0, 0.0,
            0.0, 0.0, 1.0
        ]
        navsat.position_covariance_type = NavSatFix.COVARIANCE_TYPE_APPROXIMATED

        self.publisher.publish(navsat)

def main(args=None):
    rclpy.init(args=args)
    node = GPSConverter()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()