#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from std_msgs.msg import String
from sensor_msgs.msg import PointCloud2
import pypcd
# import pcl


class hello_world():
    def __init__(self):
        # initiliaze
        rospy.init_node('pypcd_node', anonymous=False)
        self.pub_chatter = rospy.Publisher('chatter', String, queue_size=10)
        self.pub_pcd = rospy.Publisher('outcloud', PointCloud2, queue_size=10)

        pc = pypcd.PointCloud.from_path('/media/joseph/DATA_1TB/ros_bag/map.pcd')
        # p = pcl.load("/media/joseph/DATA_1TB/ros_bag/map.pcd")
        outmsg = pc.to_msg()
            # you'll probably need to set the header
        # outmsg.header = 'lidar_link'


        # How fast will we update the robot's movement?
        rate = 1.0
        # Set the equivalent ROS rate variable
        r = rospy.Rate(rate)

        while not rospy.is_shutdown():
            hello_str = "hello world %s" % rospy.get_time()
            rospy.loginfo("talker node say : "+hello_str)
            self.pub_chatter.publish(hello_str)
            self.pub_pcd.publish(outmsg)
            r.sleep()

if __name__ == '__main__':
    try:
        hello_world()
    except:
        rospy.loginfo("pypcd_node terminated.")
