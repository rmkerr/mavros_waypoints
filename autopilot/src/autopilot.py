#!/usr/bin/env python
from __future__ import print_function
import sys
import rospy
import roslib
from geometry_msgs.msg import PoseStamped
from mavros_msgs.msg import *
from mavros_msgs.srv import *

roslib.load_manifest('autopilot')
rospy.init_node('autopilot', anonymous=True)

current_state = None


def state_callback(data):
    global current_state
    print("State: "+str(data))
    current_state = data

state_sub = rospy.Subscriber("/mavros/state", State, state_callback)
local_pos_pub = rospy.Publisher("mavros/setpoint_position/local", PoseStamped, queue_size=20)
arming_client = rospy.ServiceProxy("mavros/cmd/arming", CommandBool)
set_mode_client = rospy.ServiceProxy("mavros/set_mode", SetMode)

rate = rospy.Rate(20.0)

while current_state and current_state.connected:
	rate.sleep()

pose = PoseStamped()
pose.pose.position.x = 0
pose.pose.position.y = 0
pose.pose.position.z = 2

for i in range(0,100):
	local_pos_pub.publish(pose)
	rate.sleep()

arming_client(True)
set_mode_client(custom_mode="OFFBOARD")

while True:
	local_pos_pub.publish(pose)
	rate.sleep()

try:
	rospy.spin()
except KeyboardInterrupt:
	print("Shutting down")
