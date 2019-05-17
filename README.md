# ros_vslambook

### Step 

```bash
source ~/catkin_ws_qt/devel/setup.bash
roslaunch mpu6050_6dof imu_demo.launch
cd ~/catkin_ws_qt/src/ros_vslambook/scripts
chmod +x goforward.py
chmod +x draw_a_square.py
chmod +x goincircles.py
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

```
