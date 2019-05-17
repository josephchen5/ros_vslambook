#include <ros/ros.h>
#include "std_msgs/String.h"
#include <tf/transform_broadcaster.h>


#include "sensor_msgs/Imu.h"
#include <visualization_msgs/Marker.h>

#include <iostream>
using namespace std;
geometry_msgs::Point p;
visualization_msgs::Marker line_strip;
ros::Publisher marker_pub;

sensor_msgs::Imu imuMsg;

// Eigen 部分
#include <Eigen/Core>
// Eigen 几何模块
#include <Eigen/Geometry>

// Matrix3d 实质上是 Eigen::Matrix<double, 3, 3>

Eigen::Matrix3d C,I,B,D = Eigen::Matrix3d::Zero(); //初始化为零
//Eigen::Matrix3d I = Eigen::Matrix3d::Zero(); //初始化为零
//Eigen::Matrix3d B = Eigen::Matrix3d::Zero(); //初始化为零
//Eigen::Matrix3d D = Eigen::Matrix3d::Zero(); //初始化为零

// 例如 Vector3d 实质上是 Eigen::Matrix<double, 3, 1>，即三维向量
Eigen::Vector3d ea,ab,ag,vg,sg,gg;

//Vector3d ea,ab,ag,vg,sg,gg;


bool start = false;
double interval,sigma,roll,pitch,yaw,abx,aby,abz= 0;
//double interval = 0,sigma,roll,pitch,yaw,abx,aby,abz;

int countt = 0;
//double var = 0,sum = 0, mean = 0 ;
double var,sum,mean= 0;

double count_array[100];


//void imuCallback(const std_msgs::String::ConstPtr& msg)
void imuCallback(sensor_msgs::Imu msg)
{
    //  ROS_INFO("I heard: [%s]", msg->data.c_str());
    //ROS_INFO("Hello imu!");

     if(start){
         interval = (msg.header.stamp-imuMsg.header.stamp).nsec*0.000000001;
         cout<<"T = "<<interval<<endl;

         cout<<"angular_velocity = "<<msg.angular_velocity.x<<" "<<msg.angular_velocity.y<<" "<<msg.angular_velocity.z<<endl;
         count_array[countt] = msg.angular_velocity.z;
         countt++;
         sum += count_array[countt];

         if(countt == 100){
             countt = 0;
             mean = sum/100;
             sum = 0;
             for(int i =0;i<100;i++)
             {
                     sum+=pow(count_array[i]-mean,2);
             }
             var = sum/100;
             sum = 0;
         }
         cout<<"var = "<<var<<endl;

         //variation of angles
         double wx,wy,wz;
         wx = msg.angular_velocity.x * interval;
         wy = msg.angular_velocity.y * interval;
         wz = msg.angular_velocity.z * interval;

         B <<   0, -wz,  wy,
               wz,   0, -wx,
              -wy,  wx,   0;

         cout<<"B = "<<endl<<B<<endl;


         sigma = pow(pow(wx,2)+pow(wy,2)+pow(wz,2),0.5);
         cout << "sigma = "<<sigma<<endl;

         //compute rotation matrix C
         if(sigma!=0)
                 C = C * (I + (sin(sigma)/sigma)*B + ((1-cos(sigma))/sigma/sigma)*(B*B));
         cout<<"C = "<<endl<<C<<endl;;
         //COMPUTE RPY
         ea = C.eulerAngles(0, 1, 2);
         roll = ea(0);
         pitch = ea(1);
         yaw = ea(2);
         cout<<"RPY = "<<ea[0]<<" "<<ea[1]<<" "<<ea[2]<<" "<<endl;

         //compute quaternion

         // 四元数
         // 可以直接把AngleAxis赋值给四元数，反之亦然
         Eigen::Quaterniond qu;
         qu = C;
         //cout<<"Quaternion = "<<qu.x()<<" "<<qu.y()<<" "<<qu.z()<<" "<<qu.w()<<endl;
         cout<<"Quaternion w,x,y,z= "<<qu.w()<<" "<<qu.x()<<" "<<qu.y()<<" "<<qu.z()<<endl;



         double imu_orientation_w,imu_orientation_x,imu_orientation_y,imu_orientation_z;
         imu_orientation_w = msg.orientation.w ;
         imu_orientation_x = msg.orientation.x ;
         imu_orientation_y = msg.orientation.y ;
         imu_orientation_z = msg.orientation.z ;

         cout<<"imu_Quaternion w,x,y,z= "<<imu_orientation_w<<" "<<imu_orientation_x<<" "<<imu_orientation_y<<" "<<imu_orientation_z<<endl;


         //compute position by double integration of acceleration
         abx = msg.linear_acceleration.x;
         aby = msg.linear_acceleration.y;
         abz = msg.linear_acceleration.z;
         ab << abx,aby,abz;
         ag = C*ab;
         cout<<"acc_body = "<<ab[0]<<" "<<ab[1]<<" "<<ab[2]<<" "<<endl;
         cout<<"acc_global = "<<ag[0]<<" "<<ag[1]<<" "<<ag[2]<<" "<<endl;

         vg = vg + interval*(ag-gg);
         sg = sg + interval*vg;
         cout<<"v_global = "<<vg[0]<<" "<<vg[1]<<" "<<vg[2]<<" "<<endl;
         cout<<"position_global = "<<sg[0]<<" "<<sg[1]<<" "<<sg[2]<<" "<<endl<<"-----------------------------------"<<endl;

         p.x = sg[0];
         p.y = sg[1];
         p.z = sg[2];

         //draw trajectory
         line_strip.points.push_back(p);
         marker_pub.publish(line_strip);


         //publish tf
         static tf::TransformBroadcaster br;
         tf::Transform transform1,transform2,transform3;

         transform1.setOrigin( tf::Vector3(0, 0, 0) );
         transform2.setOrigin( tf::Vector3(0, 0, 0) );
         transform3.setOrigin( tf::Vector3(0, 0, 0) );

         //transform.setOrigin( tf::Vector3(sg[0], sg[1], sg[2]) );
         tf::Quaternion q1(qu.x(),qu.y(),qu.z(),qu.w());
    //     tf::Quaternion q1(qu.w(),qu.x(),qu.y(),qu.z());

         tf::Quaternion q2;
         q2.setRPY(roll, pitch, yaw);

         tf::Quaternion q3(imu_orientation_x,imu_orientation_y,imu_orientation_z,imu_orientation_w);


         transform1.setRotation(q1);
         transform2.setRotation(q2);
         transform3.setRotation(q3);

         br.sendTransform(tf::StampedTransform(transform1, ros::Time::now(), "world", "body1_Quaternion"));
         br.sendTransform(tf::StampedTransform(transform2, ros::Time::now(), "world", "body2_RPY"));
         br.sendTransform(tf::StampedTransform(transform3, ros::Time::now(), "world", "body3_imu_orientation"));


     }
     imuMsg = msg;
     start = true;

}







int main(int argc, char **argv)
{




  //Initialization of rotation matrix,v_global,position_global
  I << 1, 0, 0,
       0, 1, 0,
       0, 0, 1;
  C = I;

  // 输出
  cout << C<< endl;


  ros::init(argc, argv, "imu_path");
  ros::NodeHandle nh;



  ros::Subscriber sub = nh.subscribe("/imu/data", 1000, imuCallback);

  marker_pub = nh.advertise<visualization_msgs::Marker>("visualization_marker", 10);

  line_strip.header.frame_id = "/world";
  line_strip.id = 0;
  line_strip.type = visualization_msgs::Marker::LINE_STRIP;
  line_strip.scale.x = 0.1;
  line_strip.color.b = 1.0;
  line_strip.color.a = 1.0;

  ros::spin();

  return 0;

}
