#!/usr/bin/env python

import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
import message_filters
from sensor_msgs.msg import LaserScan
from cv_bridge import CvBridge, CvBridgeError
from lanes_lib import getLanes


IMAGE_TOPIC = "/virat/right_camera/image_raw"
LASER_TOPIC = "/virat/laser_scan"
FUSED_TOPIC = "/virat/laser/fused"


class Node:
    def __init__(self):
        self.bridge = CvBridge()

        image_sub = message_filters.Subscriber(IMAGE_TOPIC, Image)
        laser_sub = message_filters.Subscriber(LASER_TOPIC, LaserScan)

        self.pub = rospy.Publisher(FUSED_TOPIC, LaserScan, queue_size=10)
        
        self.sync2 = message_filters.TimeSynchronizer([image_sub, laser_sub], 10)
        self.sync2.registerCallback(self.callback)

        self.dist = [1000.0 , 1000.0 ,1000.0 ,1000.0]
        self.fused_msg = LaserScan()
    
    def callback(self, image_msg, laser_msg):

        # process image data
        try:
            cv_image = self.bridge.imgmsg_to_cv2(image_msg, "bgr8")
        except CvBridgeError:
            print("ERROR : Could not process image data. Aborting...")
            quit(0)
        finally:
            final, arr = getLanes(cv_image)
        
        # fused lanes into lidar data

        self.fused_msg.ranges = list(laser_msg.ranges)
        self.fused_msg.intensities = list(laser_msg.intensities)

        for i in range(4):
            self.fused_msg.ranges[500 + (i+1) * 3] = (arr[i] * 1.465) / 79
            self.fused_msg.intensities[500 + (i+1) * 3] = (arr[i] * 1.84 * (10**20)) / 79
        
        self.fused_msg.header.seq = laser_msg.header.seq
        self.fused_msg.header.stamp.secs = laser_msg.header.stamp.secs
        self.fused_msg.header.stamp.nsecs = laser_msg.header.stamp.nsecs

        self.fused_msg.header.frame_id = laser_msg.header.frame_id
        self.fused_msg.angle_min = laser_msg.angle_min
        self.fused_msg.angle_max = laser_msg.angle_max
        self.fused_msg.angle_increment = laser_msg.angle_increment

        self.fused_msg.time_increment = laser_msg.time_increment
        self.fused_msg.scan_time = laser_msg.scan_time

        self.fused_msg.range_min = laser_msg.range_min
        self.fused_msg.range_max = laser_msg.range_max

        self.pub.publish(self.fused_msg)
        rospy.loginfo("Publishing fused data.......")


def main():
    rospy.init_node('lane_fusion', anonymous=True)

    node = Node()

    rospy.spin()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nShutting down....")
        cv2.destroyAllWindows()
        quit(0)
