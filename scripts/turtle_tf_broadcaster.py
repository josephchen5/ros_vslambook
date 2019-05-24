#!/usr/bin/env python
# -*- coding: utf-8 -*-

import roslib

import rospy

import tf

import turtlesim.msg

def broadcast_turtle_tf(data, turtlename):
    br = tf.TransformBroadcaster()
    br.sendTransform((data.x, data.y, 0),
                     tf.transformations.quaternion_from_euler(0, 0, data.theta),
                     rospy.Time.now(),
                     turtlename,
                     "world")

if __name__ == '__main__':
    rospy.init_node('turtle_tf_broadcaster')
    turtlename = rospy.get_param('~turtle')
    rospy.Subscriber('/%s/pose' % turtlename,
                     turtlesim.msg.Pose,
                     broadcast_turtle_tf,
                     turtlename)
    rospy.spin()