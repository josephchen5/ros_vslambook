# ros_vslambook

### Step 

```bash
source ~/catkin_ws_qt/devel/setup.bash
roslaunch mpu6050_6dof imu_demo.launch
cd ~/catkin_ws_qt/src/ros_vslambook/scripts
chmod +x goforward.py
chmod +x draw_a_square.py
chmod +x goincircles.py
chmod +x timed_out_and_back.py
chmod +x talker.py
chmod +x odom_out_and_back.py
chmod +x robot_tf_listener.py
chmod +x turtle_tf_broadcaster.py
chmod +x turtle_tf_listener.py
chmod +x fixed_tf_broadcaster.py
chmod +x dynamic_tf_broadcaster.py

roslaunch turtlebot_gazebo turtlebot_world.launch world_file:=/opt/ros/kinetic/share/turtlebot_gazebo/worlds/empty.world
roslaunch turtlebot_rviz_launchers view_robot.launch
```
### Step 

```bash
rosrun ros_vslambook helloword
rosrun ros_vslambook imageBasics
rosrun ros_vslambook imu_path
rosrun ros_vslambook useGeometry
rosrun ros_vslambook goforward.py
rosrun ros_vslambook draw_a_square.py
rosrun ros_vslambook goincircles.py

rosrun ros_vslambook talker.py

rosrun ros_vslambook timed_out_and_back.py
rosrun ros_vslambook turtle_tf_listener.py

rosrun ros_vslambook fixed_tf_broadcaster.py
rosrun ros_vslambook dynamic_tf_broadcaster.py



roslaunch ros_vslambook start_demo.launch

rosrun ros_vslambook robot_tf_listener.py
rosrun ros_vslambook robot_tf_listener.py


roslaunch ros_vslambook turtle_tf_broadcaster.launch

rosrun turtlesim turtlesim_node
rosrun turtlesim turtlesim_node __name:=turtle1
rosrun turtlesim turtlesim_node __name:=turtle2
rosrun turtlesim turtle_teleop_key

```
