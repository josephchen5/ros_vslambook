#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib
from actionlib_msgs.msg import *

class GoForwardAvoid():
    def __init__(self):
        rospy.init_node('nav_test', anonymous=False)

    # tell user how to stop Robot
        rospy.loginfo("To stop Robot CTRL + C")
    # What function to call when you ctrl + c
        rospy.on_shutdown(self.shutdown)


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
        goal.target_pose.header.frame_id = 'map'
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose.position.x = 3.0  # 3 meters
        goal.target_pose.pose.orientation.w = 1.0  # go forward

        # start moving
        self.move_base.send_goal(goal)

    # allow TurtleBot up to 60 seconds to complete task
        success = self.move_base.wait_for_result(rospy.Duration(60))

        if not success:
            self.move_base.cancel_goal()
            rospy.loginfo("The base failed to move forward 3 meters for some reason")
        else:
        # We made it!
            state = self.move_base.get_state()
            if state == GoalStatus.SUCCEEDED:
                rospy.loginfo("Hooray, the base moved 3 meters forward")

    def shutdown(self):
        # stop Robot
        rospy.loginfo("Stopping the robot...")
        # a default Twist has linear.x of 0 and angular.z of 0.  So it'll stop Robot
    # self.cmd_vel.publish(Twist())
        # sleep just makes sure Robot receives the stop command prior to shutting down the script
        rospy.sleep(1)


if __name__ == '__main__':
    try:
        GoForwardAvoid()
    except:
        rospy.loginfo(" GoForwardAvoid node terminated.")