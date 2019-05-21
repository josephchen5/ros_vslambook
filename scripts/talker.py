#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from std_msgs.msg import String

class hello_world():
    def __init__(self):
        # initiliaze
        rospy.init_node('talker', anonymous=True)
        self.pub = rospy.Publisher('/chatter', String, queue_size=10)

        # How fast will we update the robot's movement?
        rate = 10  # 10hz
        # Set the equivalent ROS rate variable
        r = rospy.Rate(rate)

        while not rospy.is_shutdown():
            hello_str = "hello world %s" % rospy.get_time()
            rospy.loginfo(hello_str+"  ITRI_Q200")
            self.pub.publish(hello_str)
            r.sleep()

if __name__ == '__main__':
    try:
        hello_world()
    except:
        rospy.loginfo("talker node terminated.")
