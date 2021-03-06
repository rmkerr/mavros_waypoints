#!/usr/bin/env python
from __future__ import print_function
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
arming_client = rospy.ServiceProxy("mavros/cmd/arming", CommandBool)
set_mode_client = rospy.ServiceProxy("mavros/set_mode", SetMode)

waypoint_service = rospy.ServiceProxy("mavros/mission/push", WaypointPush)

rate = rospy.Rate(20.0)

while current_state and current_state.connected:
    rate.sleep()

waypoint = Waypoint()
waypoint.x_lat = 20
waypoint.y_long = 20
waypoint.z_alt = 2
waypoint.is_current = True
waypoint.command = 16


arming_client(True)
set_mode_client(custom_mode="AUTO")

while True:
    waypoint_service(waypoint)
    rate.sleep()

try:
    rospy.spin()
except KeyboardInterrupt:
    print("Shutting down")
