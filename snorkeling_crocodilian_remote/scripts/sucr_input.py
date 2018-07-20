
import time
import pygame
from pygame.locals import *
import logging
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
import sucr_gui

class Joy:
	
	#initialization of the joystick
	def __init__(self, window_manager, config):
		#Start the pygame library
		pygame.init();

		# Setup the background scheduler
		self.config = config
		logging.basicConfig()
		self.sched = BackgroundScheduler()

		# initialize the pygame joystick library
		pygame.joystick.init()

		# Setup class variables
		self.window_manager = window_manager

		self.currJoy = None
		self.xAxis = None
		self.angularAxis = None
		self.normalDeadman = None
		self.turboButton = None
		self.armAxis = None

		self.lastReading = time.clock()
		self.lastJoyCheck = time.clock()

		self.x = 0.0
		self.angular = 0.0
		self.arm = -0.95
		self.deadman = False
		self.turbo = False

		# Give the window manager the address of this class and the update the GUI with the list of joysticks
		self.window_manager.setupJoy(self)
		self.updateJoyList()

		# Setup an interval job that checks the joystick values every 0.07 seconds
		self.sched.add_job(self.updateJoystickValues,'interval',seconds=0.05,id='get_joy')
		self.sched.start()

	# Gets a list of the joysticks and sends this list to the GUI
	def updateJoyList(self):
		self.joyList = ()
		self.joysticks = []
		if pygame.joystick.get_count() > 0:
			self.joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

		for j in self.joysticks:
			self.joyList = self.joyList + (j.get_name(),)

		self.window_manager.updateJoystickList(self.joyList)

	# When the user selects a joystick from the list, change the joystick and setup the new one, add the axis choices to the GUI
	def updateJoystickName(self,newName):
		if self.currJoy is not None:
			if self.currJoy.get_init():
				self.currJoy.quit()

		for j in self.joysticks:
			if j.get_name() == newName:
				self.currJoy = j
				self.currJoy.init()
				axisList = ()
				for ax in range(self.currJoy.get_numaxes()):
					axisList = axisList + (str(ax),)	
				buttonList = ()
				for but in range(self.currJoy.get_numbuttons()):
					buttonList = buttonList + (str(but),)

				self.window_manager.updateJoystickAxisChoices(axisList,buttonList)

	# Setters for the joystick axes and buttons
	def setXAxis(self,axis):
		self.xAxis = int(axis)

	def setAngularAxis(self,axis):
		self.angularAxis = int(axis)

	def setDeadmanButton(self,buttonNum):
		self.normalDeadman = int(buttonNum)

	def setTurboButton(self,buttonNum):
		self.turboButton = int(buttonNum)

	def setArmAxis(self,axis):
		self.armAxis = int(axis)

	# get the values from the joystick
	def updateJoystickValues(self):
		currTime = time.clock()
		if self.currJoy is not None:
			if self.currJoy.get_init():
				pygame.event.pump()
				if self.xAxis is not None:
					self.x = self.currJoy.get_axis(self.xAxis)
				if self.angularAxis is not None:
					self.angular = self.currJoy.get_axis(self.angularAxis)
				if self.normalDeadman is not None:
					self.deadman = self.currJoy.get_button(self.normalDeadman)
				if self.turboButton is not None:
					self.turbo = self.currJoy.get_button(self.turboButton)
				if self.armAxis is not None:
					self.arm = self.currJoy.get_axis(self.armAxis)
				self.lastReading = currTime
			
	# update the UI with the current joystick values
	def updateJoyUI(self):
		self.window_manager.drawJoystick(self.x,self.angular,self.deadman,self.turbo,self.arm)

	# getter for joy values
	def getJoystickValues(self):
		return joyValues(self.x,self.angular,self.deadman,self.turbo,self.arm)
	
	# Shutdown method, ends tasks
	def shutdownJoystick(self):
		self.sched.shutdown()
		pygame.quit()
			
# Class that holds the relevant values from the joystick
class joyValues(object):
	def __init__(self,x,angular,deadman,turbo,arm):
		self.x = x
		self.angular = angular
		self.deadman = deadman
		self.turbo = turbo
		self.arm = arm

if __name__ == '__main__':
	window_manager = sucr_gui.WindowManager()
	window_manager.drawWindow()
	joy = Joy(window_manager)
	atexit.register(joy.shutdownJoystick())
	window_manager.window.mainloop()
