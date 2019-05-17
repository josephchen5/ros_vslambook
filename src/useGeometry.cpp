#include "ros/ros.h"
#include "std_msgs/String.h"
#include "sensor_msgs/Imu.h"
#include <tf/transform_broadcaster.h>

#include <iostream>
using namespace std;

#include <Eigen/Core>
// Eigen 几何模块
#include <Eigen/Geometry>


void imuCallback(sensor_msgs::Imu msg)
{
  ROS_INFO("Hello imu!");
  Eigen::Matrix3d rotation_matrix = Eigen::Matrix3d::Identity();
  cout << rotation_matrix << endl;

  // 旋转向量使用 AngleAxis, 它底层不直接是Matrix，但运算可以当作矩阵（因为重载了运算符）
  Eigen::AngleAxisd rotation_vector ( M_PI/4, Eigen::Vector3d ( 0,0,1 ) );     //沿 Z 轴旋转 45 度
  cout .precision(3);
  cout<<"rotation matrix =\n"<<rotation_vector.matrix() <<endl;                //用matrix()转换成矩阵

  // 四元数
  Eigen::Quaterniond q1 = Eigen::Quaterniond ( rotation_vector );
  cout<<"quaternion x,y,z,w = \n"<<q1.coeffs() <<endl;   // 请注意coeffs的顺序是(x,y,z,w),w为实部，前三者为虚部


  //publish tf
  static tf::TransformBroadcaster br;
  tf::Transform transform1;
  transform1.setOrigin( tf::Vector3(0.1, 0.2, 0.4) );
  tf::Quaternion q(q1.x(),q1.y(),q1.z(),q1.w());
  transform1.setRotation(q);
  br.sendTransform(tf::StampedTransform(transform1, ros::Time::now(), "world", "body1"));


}

int main(int argc, char **argv)
{
  ros::init(argc, argv, "useGeometry");
  ros::NodeHandle nh;

  ros::Subscriber sub = nh.subscribe("/imu/data", 1000, imuCallback);



  ros::spin();

  return 0;
}
