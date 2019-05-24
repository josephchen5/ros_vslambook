#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import tf
import turtlesim.srv
import math
import geometry_msgs.msg


if __name__ == '__main__':
    rospy.init_node('turtle_tf_listener')
    print("test turtle_tf_listener")
    listener = tf.TransformListener()

    rospy.wait_for_service('spawn')
    spawner = rospy.ServiceProxy('spawn', turtlesim.srv.Spawn)
    spawner(4, 2, 0, 'turtle2')

    rate = rospy.Rate(10.0)
    print("I am live")


    turtle_vel = rospy.Publisher('turtle2/cmd_vel', geometry_msgs.msg.Twist,queue_size=1)

    listener.waitForTransform("/turtle2", "/carrot1", rospy.Time(), rospy.Duration(4.0))

    while not rospy.is_shutdown():
        try:
            now = rospy.Time.now() - rospy.Duration(5.0)
            listener.waitForTransform("/turtle2", "/carrot1", now, rospy.Duration(1.0))
            (trans, rot) = listener.lookupTransform("/turtle2", "/carrot1", now)
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue

        print("trans=", trans)
        print("rot=", rot)


        angular = 4 * math.atan2(trans[1], trans[0])
        linear = 0.5 * math.sqrt(trans[0] ** 2 + trans[1] ** 2)
        print("angular=", angular)
        print("linear=", linear)

        cmd = geometry_msgs.msg.Twist()
        cmd.linear.x = linear
        cmd.angular.z = angular
        turtle_vel.publish(cmd)


        rate.sleep()