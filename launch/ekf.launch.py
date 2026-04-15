from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():

    pkg_path = get_package_share_directory('localization')

    ekf_local_config = os.path.join(pkg_path, 'config', 'ekf_local.yaml')
    ekf_global_config = os.path.join(pkg_path, 'config', 'ekf_global.yaml')
    navsat_config = os.path.join(pkg_path, 'config', 'navsat.yaml')

    return LaunchDescription([


        # Local EKF (smooth odometry imu and camera)
        Node(
            package='robot_localization',
            executable='ekf_node',
            name='ekf_local',
            output='screen',
            parameters=[ekf_local_config]
        ),

        # NavSat transform (GPS conversion)
        Node(
            package='robot_localization',
            executable='navsat_transform_node',
            name='navsat_transform',
            output='screen',
            parameters=[navsat_config],
            remappings=[
                ('imu/data', '/imu/data'),
                ('gps/fix', '/gps/fix'),
                ('odometry/filtered', '/odometry/filtered')  # from ekf_local
            ]
        ),

        # Global EKF (GPS + IMU + camera)
        Node(
            package='robot_localization',
            executable='ekf_node',
            name='ekf_global',
            output='screen',
            parameters=[ekf_global_config]
        ),
    ])
