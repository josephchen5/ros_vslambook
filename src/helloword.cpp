#include <ros/ros.h>

int main(int argc, char** argv)
{
  ros::init(argc, argv, "helloword");
  ros::NodeHandle nh;

  ROS_INFO("Hello world!");
  return 0;
}
