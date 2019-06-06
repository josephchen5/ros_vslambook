#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Pose, Point, Twist, Quaternion


class MarkerBasics(object):
    def __init__(self):

        self.marker_object_pub = rospy.Publisher('/marker_basic', Marker, queue_size=1)
        self.rate = rospy.Rate(1)
        self.init_marker(index=0, x_val=1, y_val=0, z_val=0)

    def init_marker(self, index=0, x_val=0, y_val=0, z_val=0):
        self.marker_object = Marker()
        self.marker_object.header.frame_id = "odom"
        # self.marker_object.header.stamp = rospy.get_rostime()
        self.marker_object.header.stamp = rospy.Time.now()
        self.marker_object.ns = "some_robot"
        self.marker_object.id = index
        # self.marker_object.type = Marker.SPHERE
        self.marker_object.type = Marker.CUBE
        self.marker_object.action = Marker.ADD

        my_point = Point()
        my_point.x = x_val
        my_point.y = y_val
        my_point.z = z_val
        self.marker_object.pose.position = my_point

        self.marker_object.pose.orientation.x = 0
        self.marker_object.pose.orientation.y = 0
        self.marker_object.pose.orientation.z = 0.0
        self.marker_object.pose.orientation.w = 1.0

        self.marker_object.scale.x = 1.0
        self.marker_object.scale.y = 1.0
        self.marker_object.scale.z = 1.0

        self.marker_object.color.r = 0.0
        self.marker_object.color.g = 0.0
        self.marker_object.color.b = 1.0
        self.marker_object.color.a = 1.0
        marker_lifetime = 0  # 0 is forever
        self.marker_object.lifetime = rospy.Duration(marker_lifetime)

    def star(self):
        while not rospy.is_shutdown():
            hello_str = "hello world %s" % rospy.get_time()
            rospy.loginfo("talker node say : " + hello_str)
            self.marker_object_pub.publish(self.marker_object)
            self.rate.sleep()


if __name__ == '__main__':
    rospy.init_node('marker_basic_node', anonymous=True)
    marker_basic_objects=MarkerBasics()
    try:
        marker_basic_objects.star()
    except rospy.ROSInterruptException:
        pass