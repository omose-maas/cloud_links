#!/usr/bin/env python
# cording: utf-8

#
# Copyright (c) 2017, Hiroki Urase
# All rights reserved.
#

#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from socketIO_client import SocketIO
import requests, pyjsonrpc, json
from driverlesscar import Driverlesscar

class cloud_links_core:

	def __init__(self, host_url, port, rpc):
		self.host_url = host_url
		self.port = port
		self.rpc = rpc
		self.__onReady()

		self.socketIO = SocketIO(host_url, port)
		self.socketIO.on('my_request', self.on_my_resquest)


	def __onReady(self):
		request_json = pyjsonrpc.create_request_json("onReady")
		self.send_msg(request_json)

	def send_msg(self,value):
		response = requests.post(self.host_url, value)
		parsed_response = json.loads(response)
		print json.dumps(parsed_response, indent=4)

	def on_my_resquest(self.request):
		response_json = self.rpc.call(request)	
		self.socketIO.emit('my_response', response_json)


class JsonRpc(pyjsonrpc.JsonRpc):
	def __init__(self, api_obj):
		api_methods = dir(api_obj)
		apis = filter(lambda m: not m.startswith('_'), api_methods)
		[self.__setitem__(api_obj.__class__.__name__ + "." + api ,getattr(api_obj,api)) for api in apis]


def main():
	rospy.init_node('cloud_links_core', anonymous=True)

	host_url = rospy.get_param('~host_url','http://124.219.162.203')
	port = rospy.get_param('~port',5200)
	namespace = rospy.get_param('~namespace', '/post')
	status_pubfreq = rospy.get_param('~status_publish_frequency', 10)
	publish_status = rospy.get_param('~publish_status', True)


	driverlesscar = Driverlesscar()
	rpc = JsonRpc(driverlesscar)

	try:
		core = cloud_links_core(host_url, port, rpc)
		while not rospy.is_shutdown():
			if publish_status:
				request_json = pyjsonrpc.create_request_json("CarStatus",driverlesscar.get_status())
				core.send_msg(request_json)
			core.socketIO.wait(seconds = status_pubfreq)

	except rospy.ROSInterruptException:
		sock.close()
 
if __name__ == '__main__':
    main()