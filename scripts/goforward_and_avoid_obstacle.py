#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib
from actionlib_msgs.msg import *
from geometry_msgs.msg import Pose, Point, Twist, Quaternion
from math import pi
from tf.transformations import quaternion_from_euler
from visualization_msgs.msg import Marker
from visualization_msgs.msg import MarkerArray
import math

class GoForwardAvoid():
    def __init__(self):
        rospy.init_node('nav_move_base_test', anonymous=False)

    # tell user how to stop Robot
        rospy.loginfo("To stop Robot CTRL + C")
    # What function to call when you ctrl + c
        rospy.on_shutdown(self.shutdown)

        self.marker_pub = rospy.Publisher('visualization_marker_array', MarkerArray, queue_size=100)

        markerArray = MarkerArray()
        count = 0
        MARKERS_MAX = 100

        marker = Marker()
        marker.header.frame_id = "/odom"
        marker.type = marker.SPHERE
        marker.action = marker.ADD
        marker.scale.x = 0.2
        marker.scale.y = 0.2
        marker.scale.z = 0.2
        marker.color.a = 1.0
        marker.color.r = 1.0
        marker.color.g = 1.0
        marker.color.b = 0.0
        marker.pose.orientation.w = 1.0
        marker.pose.position.x = math.cos(count / 50.0)
        marker.pose.position.y = math.cos(count / 40.0)
        marker.pose.position.z = math.cos(count / 30.0)
        # We add the new marker to the MarkerArray, removing the oldest
        # marker from it when necessary
        if ( count > MARKERS_MAX ):
            markerArray.markers.pop(0)

        markerArray.markers.append(marker)

        # Renumber the marker IDs
        id = 0
        for m in markerArray.markers:
            m.id = id
            id += 1

        # Publish the MarkerArray
        self.marker_pub.publish(markerArray)

        count += 1



        # Publisher to manually control the robot (e.g. to stop it, queue_size=5)
        self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=5)
    # tell the action client that we want to spin a thread by default
        self.move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)
        rospy.loginfo("Waiting for move_base action server...")
    # Wait 60 seconds for the action server to become available
        self.move_base.wait_for_server(rospy.Duration(60))
        rospy.loginfo("Connected to move base server")
        rospy.loginfo("Starting navigation test")

    # we'll send a goal to the robot to move 3 meters forward
        goal = MoveBaseGoal()
        # goal.target_pose.header.frame_id = 'base_link'
        # goal.target_pose.header.frame_id = 'base_footprint'
        goal.target_pose.header.frame_id = 'odom'
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose.position.x = 8.0  # 3 meters
        goal.target_pose.pose.orientation.w = 1.0  # go forward

        # start moving
        self.move_base.send_goal(goal)

    # allow TurtleBot up to 60 seconds to complete task
        success = self.move_base.wait_for_result(rospy.Duration(30))

        if not success:
            self.move_base.cancel_goal()
            rospy.loginfo("The goal not success")
        else:
            # We made it!
            state = self.move_base.get_state()
            if state == GoalStatus.SUCCEEDED:
                rospy.loginfo("The goal success")

    def shutdown(self):
        # stop Robot
        rospy.loginfo("Stopping the robot...")
        self.move_base.cancel_goal()
        rospy.sleep(2)
        # a default Twist has linear.x of 0 and angular.z of 0.  So it'll stop Robot
        self.cmd_vel_pub.publish(Twist())
        # sleep just makes sure Robot receives the stop command prior to shutting down the script
        rospy.sleep(1)


if __name__ == '__main__':
    try:
        GoForwardAvoid()
    except:
        rospy.loginfo(" GoForwardAvoid node terminated.")