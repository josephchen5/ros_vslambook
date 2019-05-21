#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import math

from geometry_msgs.msg import Twist, Point, Quaternion
from math import radians, copysign, sqrt, pow, pi
import tf
import geometry_msgs.msg


if __name__ == '__main__':
    rospy.init_node('robot_tf_listener')

    listener = tf.TransformListener()

    turtle_vel = rospy.Publisher('turtle2/cmd_vel',Twist,queue_size=1)

    # How fast will we update the robot's movement?
    rate = 10  # 10hz

    #TurtleBot will stop if we don't keep telling it to move.  How often should we tell it to move? 10 HZ
    r = rospy.Rate(rate);

    while not rospy.is_shutdown():
        try:
            (trans,rot) = listener.lookupTransform('/odom', '/base_footprint', rospy.Time(0))
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            rospy.loginfo("TF Exception")
            continue

        print(trans)
        print(rot)

        angular = 4 * math.atan2(trans[1], trans[0])
        linear = 0.5 * math.sqrt(trans[0] ** 2 + trans[1] ** 2)
        cmd = geometry_msgs.msg.Twist()
        cmd.linear.x = linear
        cmd.angular.z = angular
        turtle_vel.publish(cmd)

        r.sleep()
