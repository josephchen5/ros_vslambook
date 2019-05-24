#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy

from std_msgs.msg import String

def publish_callback(event):
    hello_str = "hello world %s" % event.current_real.to_sec()
#   rospy.loginfo(hello_str)
    pub.publish(hello_str)
    now = rospy.get_rostime()
    seconds = rospy.get_time()
 #   rospy.loginfo("Current time %i secs ", now.secs)
 #   rospy.loginfo("Current time %i nsecs",now.nsecs)
    rospy.loginfo("Current time %f  secs" ,seconds)


 #   print(timer)
 #   rospy.loginfo(timer)


if __name__=='__main__':
    try:
        rospy.init_node('talker', anonymous=True)
        pub = rospy.Publisher('chatter', String, queue_size=10)
        timer = rospy.Timer(rospy.Duration(1. / 10), publish_callback)  # 10Hz
        #print(timer)


        rospy.spin()
    except rospy.ROSInterruptException:
        pass

