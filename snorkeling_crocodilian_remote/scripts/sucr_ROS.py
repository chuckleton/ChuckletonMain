#!/usr/bin/env python

import rospy
import sucr_gui
import sucr_input
import sucr_image
import sucr_data
import sucr_sensor
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32


# Config class that stores constants used throughout the program
class dataConfig:
	def __init__(self):
		self.xMax = 0.4
		self.xTurboMax = 1.0
		self.angularMax = 0.4
		self.angularTurboMax = 0.75

		self.armMax = 0.25
		self.armMin = 0.0

		self.deadzoneRadius = 0.05
		
		self.joyListRefreshTime = 0.1
		
		self.imagePath = "/home/chuckleton/catkin_ws/src/husky/snorkeling_crocodilian_remote/data/images"

	# Sets the maximum linear and angular speeds in both turbo and regular modes
	def setSpeeds(self,xMax,xTurboMax,angularMax,angularTurboMax):
		self.setXMax(xMax)
		self.setXTurboMax(xTurboMax)
		self.setAngularMax(angularMax)
		self.setAngularTurboMax(angularTurboMax)

	def setXMax(self,xMax):
		self.xMax = xMax

	def setXTurboMax(self,xTurboMax):
		self.xTurboMax = xTurboMax

	def setAngularMax(self,angularMax):
		self.angularMax = angularMax

	def setAngularTurboMax(self,angularTurboMax):
		self.angularTurboMax = angularTurboMax

# Handles ROS functions
class ROSRemote:

	# Initialize variables and sets up ROS publishers and subscribers
	def __init__(self,joystick,config,window_manager):
		self.window_manager = window_manager
		self.joystick = joystick
		self.config = config
		self.inputs = sucr_input.joyValues(0.0,0.0,0,0,0.0)
		self.node = rospy.init_node('remote_node')
		self.armCmd = Float32()
		self.armCmd.data = (self.config.armMax - self.config.armMin) / 2.0
		self.cmd_vel_publisher = rospy.Publisher('/joy_teleop/cmd_vel',Twist,queue_size=10)
		self.arm_pos_publisher = rospy.Publisher('/arduino/arm/cmd_pos',Float32,queue_size=10)
		self.image_processor = sucr_image.ImageStream(self.window_manager)
		self.status_manager = sucr_data.HuskyStatusManager(self.window_manager)
		self.sensor_manager = sucr_sensor.HuskySensorManager(self.window_manager)

	# Publishes the cmd_vel to the Husky
	def publishVelocity(self):
		self.cmd = self.getCmdVel()
		if not rospy.is_shutdown():
			self.cmd_vel_publisher.publish(self.cmd)
			self.window_manager.drawJoystick(self.cmd.linear.x,self.cmd.angular.z,self.inputs.deadman,self.inputs.turbo,self.armCmd.data)

	def publishArmPos(self):
		self.armCmd = self.getArmCmd()
		if not rospy.is_shutdown():
			self.arm_pos_publisher.publish(self.armCmd)
			
	# Gets the inputs from the joystick and converts this to a Twist message scaled correctly
	def getCmdVel(self):
		cmd_vel = Twist()
		self.inputs = self.joystick.getJoystickValues()
	
		cmd_vel.linear.y = 0.0
		cmd_vel.linear.z = 0.0
		
		cmd_vel.angular.x = 0.0
		cmd_vel.angular.y = 0.0
		
		if self.inputs.deadman == 1:
			cmd_vel.linear.x = scale(self.inputs.x,-1.0,1.0,self.config.xMax,-self.config.xMax)
			cmd_vel.angular.z = scale(self.inputs.angular,-1.0,1.0,self.config.angularMax,-self.config.angularMax)
		else:
			cmd_vel.linear.x = 0.0
			cmd_vel.linear.z = 0.0

		if self.inputs.turbo == 1: 
			cmd_vel.linear.x = scale(self.inputs.x,-1.0,1.0,self.config.xTurboMax,-self.config.xTurboMax)
			cmd_vel.angular.z = scale(self.inputs.angular,-1.0,1.0,self.config.angularTurboMax,-self.config.angularTurboMax)
		cmd_vel.linear.x = clamp(cmd_vel.linear.x,-0.99,0.99)
		cmd_vel.angular.z = clamp(cmd_vel.angular.z,-0.75,0.75)
		cmd_vel.linear.x = deadzone(cmd_vel.linear.x, self.config.deadzoneRadius)
		cmd_vel.angular.z = deadzone(cmd_vel.angular.z, self.config.deadzoneRadius)
		return cmd_vel

	def getArmCmd(self):
		arm_cmd = Float32()
		if self.inputs.deadman == 1 or self.inputs.turbo == 1:
			arm_cmd.data = scale(self.inputs.arm,-1.0,1.0,self.config.armMax,self.config.armMin)
			return arm_cmd
		else:
			return self.armCmd
		

	# Getter for current command
	def getCurrCmd(self):
		return self.cmd

	def getCurrArmCmd(self):
		return self.armCmd
		

# Scales a value from an original range to a new range
def scale(value,origLow,origHigh,newLow,newHigh):
	return (newHigh-newLow)/(origHigh-origLow)*(value-origLow) + newLow

def clamp(value,min_val,max_val):
	if value < min_val:
		return min_val
	if value > max_val:
		return max_val
	return value

def deadzone(value, radius):
	if abs(value) < radius:
		return 0.0
	return value

if __name__ == '__main__':
	window_manager = sucr_gui.WindowManager()
	window_manaer.drawWindow()
	joy = sucr_input.Joy()
	window_manager.window.mainloop()
