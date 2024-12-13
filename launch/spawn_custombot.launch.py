import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    # Set path to SDF model file
    model_folder = 'custom_bot'
    sdf_path = os.path.join(
        get_package_share_directory('medibot'),
        'models',
        model_folder,
        'model.sdf'
    )

    # Confirm that the model file exists
    if not os.path.exists(sdf_path):
        print(f"[ERROR] model.sdf file not found at path: {sdf_path}")
        return LaunchDescription()

    # Launch configuration variables for spawning location
    x_pose = LaunchConfiguration('x_pose', default='0.0')
    y_pose = LaunchConfiguration('y_pose', default='0.0')
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    # Declare launch arguments for position
    declare_x_position_cmd = DeclareLaunchArgument(
        'x_pose', default_value='0.0',
        description='X position to spawn the robot in simulation'
    )

    declare_y_position_cmd = DeclareLaunchArgument(
        'y_pose', default_value='0.0',
        description='Y position to spawn the robot in simulation'
    )

    # Spawn robot in Gazebo
    start_gazebo_ros_spawner_cmd = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-entity', 'medibot',        # Entity name in Gazebo
            '-file', sdf_path,           # Path to SDF model
            '-x', x_pose,                # X position
            '-y', y_pose,                # Y position
            '-z', '0.01'                 # Z position slightly above ground
        ],
        parameters=[{'use_sim_time': use_sim_time}],
        output='screen',
    )

    # Launch description
    ld = LaunchDescription()

    # Add launch arguments and spawner command
    ld.add_action(declare_x_position_cmd)
    ld.add_action(declare_y_position_cmd)
    ld.add_action(start_gazebo_ros_spawner_cmd)

    return ld
