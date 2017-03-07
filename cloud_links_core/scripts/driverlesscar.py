#!/usr/bin/env python
# cording: utf-8

#
# Copyright (c) 2017, Hiroki Urase
# All rights reserved.
#

#!/usr/bin/env python
import rospy
from sensor_msgs.msg import NavSatFix, NavSatStatus
from std_msgs.msg import String
import requests, pyjsonrpc, json


class DriverlessCar:
	def __init__(self,state_fix_topic):
		self.latitude = '31.253708'
		self.longitude = '130.655714'
		self.subscriber = rospy.Subscriber(state_fix_topic, NavSatFix, self.__callback)
		self.goalpub = self.publisher = rospy.Publisher('utm', NavSatFix, queue_size=50)

	def get_status(self):
		status = {'method':"get_status", 'lat' : self.latitude, 'lon' : self.longitude}
		return status

	def set_destination(self,destination):
		msg = NavSatFix()
		msg.header.stamp = rospy.get_rostime()
		msg.header.frame_id = "utm"
		msg.latitude = float(destination['latitude'])
		msg.longitude = float(destination['longitude'])
		msg.altitude = 0
		msg.status.status = NavSatStatus.STATUS_GBAS_FIX
		msg.status.service = 0
		msg.position_covariance = [0] * 9
		msg.position_covariance_type = NavSatFix.COVARIANCE_TYPE_UNKNOWN
		self.goalpub.publish(msg)
		ret = {'method':"set_position", 'msg': "got   it"}
		return ret

	def pick_user_up(self,current_location, destination):
		pass

	def __callback(self,ros_data):
		self.latitude = ros_data.latitude
		self.longitude = ros_data.longitude


if __name__ == '__main__':
	dc = DriverlessCar()
	rospy.init_node('driverless_car', anonymous=True)
	try:
		rospy.spin()
	except rospy.ROSInterruptException:
		print "Shutting down ROS driverless_car"
