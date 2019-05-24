#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from geometry_msgs.msg import Twist, Point, Quaternion
from math import radians, copysign, sqrt, pow, pi
import tf
from transform_utils import quat_to_angle, normalize_angle



class OutAndBack():
    def __init__(self):
        # initiliaze
        rospy.init_node('out_and_back', anonymous=False)

        # tell user how to stop TurtleBot
        rospy.loginfo("To stop TurtleBot CTRL + C")

        # What function to call when you ctrl + c
        rospy.on_shutdown(self.shutdown)

        # Create a publisher which can "talk" to TurtleBot and tell it to move
        # Tip: You may need to change cmd_vel_mux/input/navi to /cmd_vel if you're not using TurtleBot2
        self.cmd_vel = rospy.Publisher('cmd_vel_mux/input/navi', Twist, queue_size=10)

        # How fast will we update the robot's movement?
        rate = 20

        #TurtleBot will stop if we don't keep telling it to move.  How often should we tell it to move? 10 HZ
        r = rospy.Rate(rate);

        # 設定 out_and_back 參數

        # Set the travel distance to 1.0 meters
        goal_distance = 1.0
        # Set the forward linear speed to 0.15 meters per second
        linear_speed = 0.15
        print("設定 前進距離為%5.2f meters，速度為%5.2f m/s" % (goal_distance,linear_speed))



        # Set the rotation angle to Pi radians (180 degrees)
        goal_angle = pi
        # Set the rotation speed in radians per second
        angular_speed = 0.5
        print("設定 旋轉角度為%5.2f radians，旋轉速度為%5.2f rad/s" % (goal_angle,angular_speed))


        # Set the angular tolerance in degrees converted to radians
        angular_tolerance = radians(1.0)

        # Initialize the tf listener
        self.tf_listener = tf.TransformListener()
        # Give tf some time to fill its buffer
        rospy.sleep(2)

        # Set the odom frame
        self.odom_frame = '/odom'
        # self.odom_frame = rospy.get_param('~odom_frame', '/odom')

        self.base_frame = '/base_footprint'
        # self.base_frame = rospy.get_param('~base_frame', '/base_footprint')



        # Initialize the position variable as a Point type
        position = Point()

        for i in range(2):
            # Initialize the movement command
            move_cmd = Twist()
            # Set the movement command to forward motion
            move_cmd.linear.x = linear_speed
            (position,rotation) = self.get_odom()
            #print ("I get position =", position)
            #print ("I get rotation =", rotation)

            x_start = position.x
            y_start = position.y
            # Keep track of the distance traveled
            distance = 0
            print("distance =", distance)

            # Enter the loop to move along a side

            while distance < goal_distance and not rospy.is_shutdown():
                # Publish the Twist message and sleep 1 cycle
                self.cmd_vel.publish(move_cmd)
                r.sleep()
                # Get the current position
                (position, rotation) = self.get_odom()
                # Compute the Euclidean distance from the start
                distance = sqrt(pow((position.x - x_start), 2) +
                                pow((position.y - y_start), 2))
                print("distance =", distance)

            # Stop the robot before the rotation
            move_cmd = Twist()
            self.cmd_vel.publish(move_cmd)
            rospy.sleep(1)

            # Set the movement command to a rotation
            move_cmd.angular.z = angular_speed
            # Track the last angle measured
            last_angle = rotation
            # Track how far we have turned
            turn_angle = 0
            print("turn_angle =", turn_angle)

            while abs(turn_angle + angular_tolerance) < abs(goal_angle) and not rospy.is_shutdown():
                # Publish the Twist message and sleep 1 cycle
                self.cmd_vel.publish(move_cmd)
                r.sleep()
                # Get the current rotation
                (position, rotation) = self.get_odom()
                # Compute the amount of rotation since the last loop
                delta_angle = normalize_angle(rotation - last_angle)
                # Add to the running total
                turn_angle += delta_angle
                last_angle = rotation
                print("turn_angle =", turn_angle)

            # Stop the robot before the next leg
            move_cmd = Twist()
            self.cmd_vel.publish(move_cmd)
            rospy.sleep(1)

        # Stop the robot for good
        self.cmd_vel.publish(Twist())





    def get_odom(self):
        try:
            (trans, rot) = self.tf_listener.lookupTransform(self.odom_frame, self.base_frame, rospy.Time(0))
        except (tf.Exception, tf.ConnectivityException, tf.LookupException):
            rospy.loginfo("TF Exception")
            return
        #print("I get_odom trans=", trans)
        #print("I get_odom rot=", rot)
        return (Point(*trans), quat_to_angle(Quaternion(*rot)))



    def shutdown(self):
        # stop turtlebot
        rospy.loginfo("Stop the robot")
        # a default Twist has linear.x of 0 and angular.z of 0.  So it'll stop TurtleBot
        self.cmd_vel.publish(Twist())
        # sleep just makes sure TurtleBot receives the stop command prior to shutting down the script
        rospy.sleep(2)

if __name__ == '__main__':
    try:
        OutAndBack()
    except:
        rospy.loginfo("Out-and-Back node terminated.")

