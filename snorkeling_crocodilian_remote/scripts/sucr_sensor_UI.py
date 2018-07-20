
import rospy

from sensor_msgs.msg import Imu
from sensor_msgs.msg import Range
from std_msgs.msg import Bool
from std_msgs.msg import Float32

import Tkinter as tk
from ttk import *


# This class handles the user interfaces for everything connected to the Arduino
# includes: 
# Stepper motor (arm)
# Limit switch (arm)
# IMU
# Rangefinder

class SensorUIHandler:
	
	def __init__(self, window_manager, status_tab, drive_tab, config_tab, config):

		self.window_manager = window_manager
		self.status_tab = status_tab
		self.drive_tab = drive_tab
		self.config_tab = config_tab

		self.config = config

		self.armVisSlider = tk.Scale(self.drive_tab,from_=self.config.armMin,to=self.config.armMax,orient=tk.HORIZONTAL,resolution=0.01,state='disabled',label="Arm Value",length = 250,sliderlength=10)
		self.armVisSlider.grid(column = 1,row = 11)

	def updateArmSlider(self, value):	
		self.armVisSlider.config(state='normal')
		self.armVisSlider.set(value)
		self.armVisSlider.config(state='disabled')

	def updateArmCurrPos(self, armData):
		pass

	def updateIMU(self, imuData):
		pass

	def updateRange(self, rangeData):
		pass

	def updateLimit(self, limitData):
		pass

		
