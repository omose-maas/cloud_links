#!/usr/bin/env python
# cording: utf-8

#
# Copyright (c) 2017, Hiroki Urase
# All rights reserved.
#

#!/usr/bin/env python
import rospy
import tf2_ros
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseStamped

class utm_simple_goal:
	def __init__(self,utm_odom_topic):
		self.utm_odom = rospy.Subscriber(utm_odom_topic, Odometry, self.callback)
		self.publisher = rospy.Publisher('move_base_simple/goal', PoseStamped, queue_size=50)
		
		#tf2 setup
		tfBuffer = tf2_ros.tfBuffer()
		self.tfListener = tf2_ros.TransformListener(tfBuffer)

	def callback(self):

	def publish_goal(self):



def main():
	rospy.init_node('utm_simple_goal', anonymous=True)

	#Get Parameters
	utm_odom_topic = rospy.get_param('~utm_odom_topic', "odom/goal")

	simple_goal = utm_simple_goal(utm_odom_topic)

	
 
if __name__ == '__main__':
    main()