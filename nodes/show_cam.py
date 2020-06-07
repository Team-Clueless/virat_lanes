#!/usr/bin/env python

import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from lanes_lib.main import processImage


class ImageConv:
  def __init__(self):

    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("/virat/right_camera/image_raw",Image,self.callback)

  def callback(self,data):
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
      print(e)
    
    # the camera frame is fed into processImage function in the lanes_lib package module
    final = processImage(cv_image)
    # Lane lines detection and process cross track error
    cv2.imshow("lanes", final)
    cv2.waitKey(3)


def main():
  ic = ImageConv()
  rospy.init_node('image_converter', anonymous=True)
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
  cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
