#!/usr/bin/env python
from __future__ import print_function
import rospy
import roslib
import os
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
arming_client = rospy.ServiceProxy("mavros/cmd/arming", CommandBool)
set_mode_client = rospy.ServiceProxy("mavros/set_mode", SetMode)

rate = rospy.Rate(20.0)

while current_state and current_state.connected:
    rate.sleep()

os.system("rosrun mavros mavwp load //home//$USER//local_ws//waypoints.txt")

arming_client(True)
set_mode_client(custom_mode="AUTO")

try:
    rospy.spin()
except KeyboardInterrupt:
    print("Shutting down")
