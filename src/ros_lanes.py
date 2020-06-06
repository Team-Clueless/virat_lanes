#!/usr/bin/env python
from __future__ import print_function

# import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from distance_indice import find_marker
from sensor_msgs.msg import LaserScan
#from change_laser_data import changer




class image_converter:
  def __init__(self):
    self.bridge=CvBridge()
    self.image_sub=rospy.Subscriber("/virat/right_camera/image_raw",Image,self.callback)
    self.laser_scan=rospy.Subscriber('/virat/laser_scan', LaserScan , self.bro)
    
    self.dist = [1000.0 , 1000.0 ,1000.0 ,1000.0]
    self.modified = LaserScan()
    self.laser = rospy.Publisher('/virat/laser/sn' ,LaserScan ,10)

  def bro(self,msg):
    
    self.modified.ranges = list(msg.ranges)
    self.modified.intensities = list(msg.intensities)
    for j in range (0,4):
      self.modified.ranges[500+(j+1)*3] = (self.arr[j]*1.465)/79
      self.modified.intensities[500+(j+1)*3] = (self.arr[j]*(1.84*(10**20)))/79

    self.modified.header.seq = msg.header.seq
    self.modified.header.stamp.secs = msg.header.stamp.secs
    self.modified.header.stamp.nsecs = msg.header.stamp.nsecs
    self.modified.header.frame_id = msg.header.frame_id
    self.modified.angle_min = msg.angle_min
    self.modified.angle_max = msg.angle_max
    self.modified.angle_increment = msg.angle_increment
    self.modified.time_increment = msg.time_increment
    self.modified.scan_time = msg.scan_time
    self.modified.range_min = msg.range_min
    self.modified.range_max = msg.range_max
    self.laser.publish(self.modified)

    
    print(self.modified)



  def callback(self,data):
    try:
      cv_image=self.bridge.imgmsg_to_cv2(data,"bgr8")
    except CvBridgeError as e:
      print(e)

    #link to the other files that will run

    final,self.arr = find_marker(cv_image)
    


    


    #display image 
    cv2.imshow("lanes",final)   #final consists of post processed image
    cv2.waitKey(3)
    

    

def main():
  ic=image_converter()
  rospy.init_node("image_converter",anonymous=True)
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
  cv2.destroyAllWindows()

if __name__ == '__main__':
  main()