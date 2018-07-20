#!/usr/bin/env python

import rospy
import sucr_gui
import sucr_input
import sucr_ROS
import time
from apscheduler.schedulers.background import BackgroundScheduler

import sys

# Master class that controls all the other classes
class Master:
	
	# Initialize all of the needed functions
	def __init__(self):
		# Scheduler to run various functions while GUI is looping
		self.sched = BackgroundScheduler()

		# Setup the config file
		self.config = sucr_ROS.dataConfig()

		# Setup the GUI, run shutdown method on close
		self.window_manager = sucr_gui.WindowManager(self.config)
		self.window_manager.window.protocol("WM_DELETE_WINDOW",self.shutdown)
		self.window_manager.drawWindow()
	
		# Setup the joystick input (will setup scheduled joystick readings)
		self.joy = sucr_input.Joy(self.window_manager,self.config)

		# Setup the ROS node
		self.rosRemote = sucr_ROS.ROSRemote(self.joy,self.config,self.window_manager)

	# Class that starts the whole process running, schedules update tasks and then loops GUI
	def run(self):  
		self.sched.add_job(self.updateROS,'interval',seconds=0.05,id='run_ros')
		self.sched.start()
		# Main loop for Tkinter GUI, blocking method
		# Program will remain here until shutdown
		self.window_manager.window.mainloop()

	# Scheduled task, runs ROS functions
	def updateROS(self):
		# Make sure that the ROS node still exists
		if not rospy.is_shutdown():
			try:
				# Publish the velocity commands
				self.rosRemote.publishVelocity()
				# Publish the arm position command
				self.rosRemote.publishArmPos()
			except rospy.ROSInterruptException:
				pass

	# Runs on shutdown, allows graceful close
	# Make sure that joystick is shutdown AFTER main scheduler otherwise
	# main scheduler will get stuck in a thread without joystick data and will 
	# not finish shut down
	def shutdown(self):
		self.sched.shutdown()
		self.joy.shutdownJoystick()
		self.window_manager.window.destroy()
	
if __name__ == '__main__':
	
	master = Master()
	master.run()
