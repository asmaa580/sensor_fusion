from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():

    config = os.path.join(
        get_package_share_directory('localization'),
        'config',
        'ekf.yaml'
    )

    return LaunchDescription([

        Node(
            package='robot_localization',
            executable='ekf_node',
            name='ekf_filter_node',
            output='screen',
            parameters=[config]
        ),
        
         # NavSat transform
        Node(
            package='robot_localization',
            executable='navsat_transform_node',
            name='navsat_transform',
            parameters=['navsat.yaml'],
            remappings=[
                ('imu/data', '/imu/data'),
                ('gps/fix', '/fix')
            ]
        ),

    ])